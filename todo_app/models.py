from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model): # আমাদের টাস্ক মডেল, যা টাস্কের তথ্য সংরক্ষণ করবে
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # এই লাইনটি যোগ করো
    title = models.CharField(max_length=200) # টাস্কের নাম
    description = models.TextField()           # বিস্তারিত
    category = models.CharField(max_length=20, default='General') # টাস্কের ক্যাটাগরি, ডিফল্ট মান 'General'
    due_date = models.DateTimeField(null=True, blank=True) # টাস্কের শেষ সময়, null=True এবং blank=True মানে এই ফিল্ডটি খালি থাকতে পারে
    is_completed = models.BooleanField(default=False) # সম্পন্ন হয়েছে কি না
    created_at = models.DateTimeField(auto_now_add=True) # তৈরির সময়
    is_missed = models.BooleanField(default=False) # এই ফিল্ডটি চিহ্নিত করবে যে টাস্কটি শেষ সময় পার হয়ে গেছে কিনা

# Note Model 
class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
