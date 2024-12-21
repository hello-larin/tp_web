from .models import *
from django import forms

class LoginForm(forms.ModelForm):
    check_password = forms.PasswordInput(("Пароль"))
    password = forms.PasswordInput(("Пароль"))
    username = forms.CharField(("Логин"), max_length=128)
    class Meta:
        model = User
        fields = ("username", "password")


class RegisterForm(forms.ModelForm):
    check_password = forms.PasswordInput("Пароль")
    password = forms.PasswordInput("Пароль")
    username = forms.CharField("Логин", max_length=128)
    email = forms.EmailField("Почта")
    class Meta:
        model = User
        fields = ("username", "email", "password")


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ("title", "text", "tags")


class SettingsForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("user__username", "user__email", "avatar", "nickname")


class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ("description",)

