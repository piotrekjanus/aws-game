from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.utils.html import strip_tags
# Create your views here.
import re
from django.utils.html import escape


def home_view(request):
    return render(request, 'index.html', {})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created for {}'.format(request.POST['username']))
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'login/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST or None)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')
        else:
            messages.error(request, list(form.error_messages.values()))
    else:
        form = AuthenticationForm()
    context = {'form': []}
    return render(request, 'login/login.html', context)
