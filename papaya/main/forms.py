from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['password'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Имя пользователя'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})

    class Meta:
        model = User
        fields = ['username', 'password']


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].label = ''
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Имя пользователя'})
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = ''
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Пароль'})
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = ''
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control',
                                                                     'placeholder': 'Подтвердите пароль'})