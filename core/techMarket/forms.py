from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Unit
from captcha.fields import CaptchaField


class UnitForm(forms.ModelForm):
    title = forms.CharField(label='Наименование')
    about = forms.CharField(label='Описание')
    characters = forms.CharField(label='Характеристики')
    price = forms.IntegerField(label='Цена')
    photo = forms.ImageField(label='Фото')
    class Meta:
        model = Unit
        fields = ['title','about','character','price','photo','cat']
        widjets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'about': forms.Textarea(attrs={'class': 'form-input'}),
            'character': forms.Textarea(attrs={'class': 'form-input'}),
        }

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widjets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    captcha = CaptchaField()
