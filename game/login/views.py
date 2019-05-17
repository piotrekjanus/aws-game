from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.html import strip_tags
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
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
            messages.error(request, mess[0][0]['message'])
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
            mess = list(form.errors.get_json_data().values())
            # print(mess[0][0]['message'])
            messages.error(request, mess[0][0]['message'])
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login/login.html', context)


def logout_view(request):
    logout(request)
    messages.warning(request, 'You have been logged out')
    return redirect('login')
