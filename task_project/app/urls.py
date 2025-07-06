from django.urls import path
from .views import(
    ProjectListView, TaskListView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView
)

app_name = 'app'

urlpatterns = [
    path('project_list/', ProjectListView.as_view(), name='project_list'),
    path('task/<int:pk>', TaskListView.as_view(), name='task'),
    path('add_project/', ProjectCreateView.as_view(), name='add_project'),
    path('update_project/<int:pk>', ProjectUpdateView.as_view(), name='update_project'),
    path('delete_project/<int:pk>', ProjectDeleteView.as_view(), name='delete_project'),
]
