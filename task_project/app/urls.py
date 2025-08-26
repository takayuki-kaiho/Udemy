from django.urls import path
from .views import(
    DashboardView, ProjectListView, TaskListView,
    ProjectCreateView, ProjectUpdateView, ProjectDeleteView,
    TaskCreateView, TaskUpdateView, TaskDeleteView,
)

app_name = 'app'

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path('project_list/', ProjectListView.as_view(), name='project_list'),
    path('task/<int:project_id>/', TaskListView.as_view(), name='task'),
    path('add_project/', ProjectCreateView.as_view(), name='add_project'),
    path('update_project/<int:pk>/', ProjectUpdateView.as_view(), name='update_project'),
    path('delete_project/<int:pk>/', ProjectDeleteView.as_view(), name='delete_project'),
    path('add_task/<int:project_id>/', TaskCreateView.as_view(), name='add_task'),
    path('update_task/<int:pk>/', TaskUpdateView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', TaskDeleteView.as_view(), name='delete_task'),
]
