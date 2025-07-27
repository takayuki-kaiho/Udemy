from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

# class UserUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
        
        
class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(),
        required=False,  # 入力がなければ変更しないように
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': '名前',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password, self.instance)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)  # プレーンパスワードをハッシュ化
        if commit:
            user.save()
        return user

class RegistForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'username': '名前',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        user = User(
            username=cleaned_data.get('username'),
            email=cleaned_data.get('email'),
        )

        if password:
            try:
                validate_password(password, user)
            except ValidationError as e:
                self.add_error('password', e)

        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    # email = forms.EmailField(label='メールアドレス')
    # password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    email = forms.EmailField(
        label='メールアドレス',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class UserLoginForm2(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='セッションの時間を長くする', required=False)
