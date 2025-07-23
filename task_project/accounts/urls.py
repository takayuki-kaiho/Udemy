from django.urls import path
from . import views
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserLoginView2,
    UserLogoutView2, UserUpdateView,
)

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='register'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', views.UserUpdateView.as_view(), name='user_update'),
    path('user_login_2/', UserLoginView2.as_view(), name='user_login_2'),
    path('user_logout_2/', UserLogoutView2.as_view(), name='user_logout_2'),
]