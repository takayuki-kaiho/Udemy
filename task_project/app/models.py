from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     user_name = models.CharField(max_length=50)
#     user_mail = models.EmailField()
#     user_password = models.CharField(max_length=32)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'user'
      
#     def __str__(self):
#         return self.user_name
      
      
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    user_id =models.ForeignKey(
        # User,
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='projects',
    )
    project_name = models.CharField(max_length=100)
    scheduled_start = models.DateTimeField(null=True, blank=True)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    achievement_start = models.DateTimeField(null=True, blank=True)
    achievement_end =models.DateTimeField(null=True, blank=True)
    
    STATUS_CHOICES = [
    ('not_started', '未着手'),
    ('in_progress', '進行中'),
    ('completed', '完了'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project'
      
    def __str__(self):
        return self.project_name


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    project_id =models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    task_name = models.CharField(max_length=100)
    scheduled_start = models.DateTimeField(null=True, blank=True)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    achievement_start = models.DateTimeField(null=True, blank=True)
    achievement_end =models.DateTimeField(null=True, blank=True)
    
    STATUS_CHOICES = [
    ('not_started', '未着手'),
    ('in_progress', '進行中'),
    ('completed', '完了'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'task'
      
    def __str__(self):
        return self.task_name
    