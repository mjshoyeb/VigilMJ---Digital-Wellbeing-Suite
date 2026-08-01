from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm 
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone as django_timezone
from datetime import datetime  # সরাসরি ব্যাকআপের জন্য
from .models import Note 


# ----------------------------------------------------
# 🏠 হোম ড্যাশবোর্ড ইঞ্জিন (Dashboard Core View)
# ----------------------------------------------------
@login_required(login_url='login')
def home(request):
    search_input = request.GET.get('search-area') or ''
    # 🔄 LIFO স্টাইলে সাজানোর জন্য সংশোধন (নতুন টাস্ক সবার উপরে থাকবে)
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
    # পেন্ডিং মানে যা সম্পন্নও হয়নি, আবার সময়ও শেষ হয়ে যায়নি
    pending_count = all_tasks.filter(is_completed=False, is_missed=False).count()

    # 🟢 ৩. প্রোগ্রেস বার পার্সেন্টেজ (%) ম্যাথমেটিক্যাল ক্যালকুলেশন
    progress_percentage = 0
    if total_tasks_count > 0:
        progress_percentage = int((completed_count / total_tasks_count) * 100)

    # টাস্ক সার্চ ফিল্টারিং অপারেশন
    tasks = all_tasks
    if search_input:
        tasks = tasks.filter(title__icontains=search_input)
        
    # নতুন টাস্ক ক্রিয়েশন পোস্ট রিকোয়েস্ট হ্যান্ডলিং
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.due_date = request.POST.get('due_date') or None
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
        
    # 🟢 ৪. ফ্রন্টএন্ড গ্লাস-UI তে পাঠানোর জন্য কনটেক্সট ডিকশনারি
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
    # নিরাপত্তার জন্য get_object_or_404 এবং user=request.user ব্যবহার করা হয়েছে
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete() 
    return redirect('home') 


# ----------------------------------------------------
# ✅ টাস্ক সম্পন্ন করার ইঞ্জিন (Complete View)
# ----------------------------------------------------
@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = True # সম্পন্ন স্ট্যাটাস ফ্ল্যাগ ট্রু করা হলো
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
            updated_task = form.save(commit=False)
            
            # 🟢 এডিট প্যানেল থেকে নতুন ডেডলাইন রিসিভ এবং প্রসেস করা
            due_date_input = request.POST.get('due_date')
            updated_task.due_date = due_date_input if due_date_input else None
            
            updated_task.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task) 
        
    return render(request, 'edit_task.html', {'form': form, 'task': task})


# ----------------------------------------------------
# 🔐 ইউজার সিকিউরিটি ও গেটওয়ে (Authentication Views)
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
            login(self.request, user) # রেজিস্ট্রেশন সফল হলে অটো-লগইন প্রোটেকশন
        return super(RegisterPage, self).form_valid(form)

# Notepad functionality views
@login_required
def note_list(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            Note.objects.create(user=request.user, title=title, content=content)
            return redirect('note_list')
            
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes.html', {'notes': notes})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.delete()
    return redirect('note_list')