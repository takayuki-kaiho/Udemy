from django.shortcuts import render
from django.views.generic import(
    ListView, CreateView, UpdateView, DeleteView
)

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import(
    Project, Task
)
from django.urls import reverse_lazy
from django.utils.functional import SimpleLazyObject

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'app/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        query = super().get_queryset()
        project_name = self.request.GET.get('project_name')
        project_status = self.request.GET.get('status')
        if project_name:
            query = query.filter(
                project_name=project_name
            )
        if project_status:
            query = query.filter(
                status=project_status
            )
        scheduled_start =self.request.GET.get('scheduled_start', '0')
        if scheduled_start == '1':
            query = query.order_by('scheduled_start')
        elif scheduled_start == '2':
            query = query.order_by('-scheduled_start')
        else:
            query = query.order_by('-id')
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name'] = self.request.GET.get('project_name', '')
        context['status'] = self.request.GET.get('status', '')
        scheduled_start = self.request.GET.get('scheduled_start', '0')
        context['scheduled_start'] = scheduled_start
        context['ascending'] = scheduled_start == '1'
        context['descending'] = scheduled_start == '2'
        return context

#タスク
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'app/task.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        query = super().get_queryset()
        task_name = self.request.GET.get('task_name')
        task_status = self.request.GET.get('status')
        if task_name:
            query = query.filter(
                task_name=task_name
            )
        if task_status:
            query = query.filter(
                status=task_status
            )
        scheduled_start =self.request.GET.get('scheduled_start', '0')
        if scheduled_start == '1':
            query = query.order_by('scheduled_start')
        elif scheduled_start == '2':
            query = query.order_by('-scheduled_start')
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_name'] = self.request.GET.get('task_name', '')
        context['status'] = self.request.GET.get('status', '')
        scheduled_start = self.request.GET.get('scheduled_start', '0')
        context['scheduled_start'] = scheduled_start
        context['ascending'] = scheduled_start == '1'
        context['descending'] = scheduled_start == '2'
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['project_name', 'scheduled_start', 'sheduled_end', 'achievement_start', 'achievement_end', 'status']
    template_name = 'app/add_project.html'
    success_url = reverse_lazy('app:project_list')
    
    def form_valid(self, form):
        form.instance.user_id = self.request.user 
        return super().form_valid(form)
    

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['project_name', 'scheduled_start', 'sheduled_end', 'achievement_start', 'achievement_end', 'status']
    template_name = 'app/update_project.html'
    def get_success_url(self):
        return reverse_lazy('app:project_list', kwargs={'user_id': UpdateView.object.pk})

class ProjectDeleteView(UpdateView):
    model = Project
    fields = ['project_name']
    template_name = 'app/delete_project.html'
    success_url = reverse_lazy('app:project_list')
