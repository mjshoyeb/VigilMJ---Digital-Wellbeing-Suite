"""
URL configuration for my_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

# দুটি আলাদা নাম দিয়ে ইম্পোর্ট করো
from my_site import views as main_views 
from todo_app import views as todo_views

# ইউজার অথেন্টিকেশন ভিউ ইম্পোর্ট করো
from django.contrib.auth.views import LogoutView 
from todo_app.views import CustomLoginView, RegisterPage 
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # টাস্ক লিস্টের জন্য todo_app এর views ব্যবহার করো
    path('todo/', todo_views.home, name='todo'), 
    
    # About এবং Contact এর জন্য main_views ব্যবহার করো
    path('about/', main_views.about, name='about'),
    path('contact/', main_views.contact, name='contact'),
    
    # তুমি চাইলে মেইন হোম পেজ হিসেবেও todo লিস্ট দেখাতে পারো
    path('', todo_views.home, name='home'),

    path('delete/<int:task_id>/', todo_views.delete_task, name='delete_task'),
    path('complete/<int:task_id>/', todo_views.complete_task, name='complete_task'),
    path('edit/<int:task_id>/', todo_views.edit_task, name='edit_task'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('notes/', todo_views.note_list, name='note_list'),
    path('notes/delete/<int:note_id>/', todo_views.delete_note, name='delete_note'),
]