from django.shortcuts import render, redirect
from django.views.generic import(
    TemplateView, CreateView, FormView, View
)
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from .forms import RegistForm, UserLoginForm, UserLoginForm2
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import UserUpdateForm
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()


class HomeView(FormView):
    # template_name = 'home.html'
    template_name = 'home.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('app:project_list')

    # def form_valid(self, form):
    #     email = form.cleaned_data['email']
    #     password = form.cleaned_data['password']
    #     try:
    #         user_obj = User.objects.get(email=email)
    #         user = authenticate(self.request, username=user_obj.username, password=password)
    #     except User.DoesNotExist:
    #         user = None

    #     if user is not None:
    #         login(self.request, user)
    #         return super().form_valid(form)
    #     form.add_error(None, "メールアドレスかパスワードが正しくありません。")
    #     return self.form_invalid(form)
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
    
        form.add_error(None, "メールアドレスかパスワードが正しくありません。")
        return self.form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_nav'] = True
        return context

    
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  # 明示的にここでも呼ぶ
        user.save()
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'  # このテンプレートを作成する必要があります
    success_url = reverse_lazy('app:project_list')  # 適宜変更してください

    def get_object(self):
        return self.request.user  # ログインユーザーの情報を編集する
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # 🔽 パスワードが変わった後もセッションを維持（再認証）
        update_session_auth_hash(self.request, self.object)
        return response

class UserLoginView(FormView):
    template_name = 'user_login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('accounts:home')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(self.request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(self.request, user)
            return super().form_valid(form)

        form.add_error(None, "メールアドレスかパスワードが正しくありません。")
        return self.form_invalid(form)

    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        print('next: ', next_url)
        return next_url if next_url else self.success_url

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_logout.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:home')


class UserLoginView2(LoginView):
    template_name = 'user_login_2.html'
    next_page = reverse_lazy('accounts:home')
    form_class = UserLoginForm2
    
    def form_valid(self, form):
        result = super().form_valid(form)
        print(self.request.user)
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(1200000)
        return result


class UserLogoutView2(LogoutView):
    next_page = reverse_lazy('accounts:home')
    http_method_names = ['get', 'post']
    template_name = 'user_logout.html'


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録と同時にログイン
            return redirect('accounts:home')  # 遷移先はお好みで
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
