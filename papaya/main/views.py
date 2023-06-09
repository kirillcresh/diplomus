from django.shortcuts import render, redirect
from .forms import *
from .forms import UserCreationForm
from django.template import loader
from django.contrib.auth import login
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpRequest
from datetime import datetime
from news.models import News


class Login(LoginView):
    fields = ['username', 'password']
    template_name = 'main/login.html'
    form_class = AuthUserForm


def register(request):
    assert isinstance(request, HttpRequest)
    form = UserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            reg_form = form.save(commit=False)
            reg_form.is_staff = False
            reg_form.is_superuser = False
            reg_form.date_joined = datetime.now()
            reg_form.last_login = datetime.now()
            reg_form.is_active = True
            reg_form.save()
            reg_form.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, reg_form)
            return render(request, 'main/index.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


class Logout(LogoutView):
    template_name = 'main/index.html'


def index(request):
    last_news = News.objects.order_by('-pub_date')[:3]
    context = {
        'last_news': last_news,
    }
    return render(request, 'main/index.html', context)


def contacts(request):
    return render(request, 'main/contacts.html')


def about(request):
    return render(request, 'main/about.html')


def manage(request):
    if request.user.is_staff:
        return render(request, 'main/manager.html')
    else:
        return redirect('main:main')
