from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

      
class Project(models.Model):
    id = models.AutoField(primary_key=True)
    
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='ユーザー'
    )
    
    project_name = models.CharField('プロジェクト名', max_length=100)
    scheduled_start = models.DateTimeField('開始予定日', null=True, blank=True)
    scheduled_end = models.DateTimeField('終了予定日', null=True, blank=True)
    achievement_start = models.DateTimeField('開始実績日', null=True, blank=True)
    achievement_end = models.DateTimeField('終了実績日', null=True, blank=True)

    STATUS_CHOICES = [
        ('未着手', '未着手'),
        ('進行中', '進行中'),
        ('完了', '完了'),
    ]
    status = models.CharField('ステータス', max_length=50, choices=STATUS_CHOICES)
    
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    
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
    task_name = models.CharField('タスク名', max_length=100)
    scheduled_start = models.DateTimeField('開始予定日', null=True, blank=True)
    scheduled_end = models.DateTimeField('終了予定日', null=True, blank=True)
    achievement_start = models.DateTimeField('開始実績日', null=True, blank=True)
    achievement_end = models.DateTimeField('終了実績日', null=True, blank=True)
    
    STATUS_CHOICES = [
    ('未着手', '未着手'),
    ('進行中', '進行中'),
    ('完了', '完了'),
    ]
    status = models.CharField('ステータス', max_length=50, choices=STATUS_CHOICES)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'task'
      
    def __str__(self):
        return self.task_name
    