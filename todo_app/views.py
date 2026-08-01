from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone as django_timezone
from django.db.models import Q
from django.contrib import messages
from datetime import datetime

from .models import Task, Note 
from .forms import TaskForm 


# ----------------------------------------------------
# 🏠 হোম ড্যাশবোর্ড ইঞ্জিন (Dashboard Core View)
# ----------------------------------------------------
@login_required(login_url='login')
def home(request):
    search_input = request.GET.get('search-area') or ''
    # 🔄 LIFO স্টাইলে সাজানোর জন্য (নতুন টাস্ক সবার উপরে থাকবে)
    all_tasks = Task.objects.filter(user=request.user).order_by('-id')
    
    # 🟢 ১. ব্যাকএন্ডে ডেডলাইন চেক করে Missed স্ট্যাটাস লাইভ লক করা
    current_time = django_timezone.now() 
    
    for task in all_tasks:
        if not task.is_completed and not task.is_missed and task.due_date and task.due_date < current_time:
            task.is_missed = True
            task.save()

    # 🟢 ২. ড্যাশবোর্ড কাউন্টার কার্ডের জন্য ডেটা প্রসেসিং
    total_tasks_count = all_tasks.count()
    completed_count = all_tasks.filter(is_completed=True).count()
    missed_count = all_tasks.filter(is_missed=True).count()
    pending_count = all_tasks.filter(is_completed=False, is_missed=False).count()

    # 🟢 ৩. প্রোগ্রেস বার পার্সেন্টেজ (%) ক্যালকুলেশন
    progress_percentage = 0
    if total_tasks_count > 0:
        progress_percentage = int((completed_count / total_tasks_count) * 100)

    # টাস্ক সার্চ ফিল্টারিং
    tasks = all_tasks
    if search_input:
        tasks = tasks.filter(title__icontains=search_input)
        
    # নতুন টাস্ক ক্রিয়েশন হ্যান্ডলিং
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            due_date_str = request.POST.get('due_date')
            
            # 🛡️ অতীতের সময় বা ডেট সিলেক্ট করা ঠেকানোর জন্য ভ্যালিডেশন
            if due_date_str:
                selected_date = datetime.fromisoformat(due_date_str)
                # Naive datetime কে timezone aware এ রূপান্তর
                if django_timezone.is_naive(selected_date):
                    selected_date = django_timezone.make_aware(selected_date)
                
                if selected_date < current_time:
                    messages.error(request, "Deadline cannot be set in the past! Please choose a future date.")
                    return redirect('home')

            task = form.save(commit=False)
            task.user = request.user
            task.due_date = due_date_str or None
            task.save()
            messages.success(request, "Task created successfully!")
            return redirect('home')
    else:
        form = TaskForm()
        
    context = {
        'tasks': tasks,
        'form': form,
        'search_input': search_input,
        'total_tasks': total_tasks_count,
        'completed_count': completed_count,
        'missed_count': missed_count,
        'pending_count': pending_count,
        'progress': progress_percentage,
    }
    return render(request, 'index.html', context)


# ----------------------------------------------------
# 🗑️ টাস্ক ডিলিট ইঞ্জিন (Secure Delete View)
# ----------------------------------------------------
@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete() 
    return redirect('home') 


# ----------------------------------------------------
# ✅ টাস্ক সম্পন্ন করার ইঞ্জিন (Complete View)
# ----------------------------------------------------
@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True
    task.save() 
    return redirect('home')


# ----------------------------------------------------
# 📝 টাস্ক এডিট ও আপডেট কনফিগারেশন (Edit View)
# ----------------------------------------------------
@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user) 
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task) 
        if form.is_valid():
            due_date_input = request.POST.get('due_date')
            current_time = django_timezone.now()

            # 🛡️ অতীতের ডেট ভ্যালিডেশন (এডিট পেজের জন্য)
            if due_date_input:
                selected_date = datetime.fromisoformat(due_date_input)
                if django_timezone.is_naive(selected_date):
                    selected_date = django_timezone.make_aware(selected_date)
                
                if selected_date < current_time:
                    messages.error(request, "Deadline cannot be updated to a past date!")
                    return render(request, 'edit_task.html', {'form': form, 'task': task})

            updated_task = form.save(commit=False)
            updated_task.due_date = due_date_input if due_date_input else None
            updated_task.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task) 
        
    return render(request, 'edit_task.html', {'form': form, 'task': task})


# ----------------------------------------------------
# 🔐 ইউজার সিকিউরিটি ও গেটওয়ে (Authentication Views)
# ----------------------------------------------------
class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


# ----------------------------------------------------
# 📑 কুইক নোটস ইঞ্জিন (Notepad Functionality Views)
# ----------------------------------------------------
@login_required
def note_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            return redirect('note_list')

    query = request.GET.get('search', '').strip()
    notes = Note.objects.filter(user=request.user)

    if query:
        notes = notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    notes = notes.order_by('-created_at')

    return render(request, 'notes.html', {
        'notes': notes,
        'search_query': query
    })

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('note_list')