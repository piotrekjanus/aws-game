from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Result
from django.db.models import Q

@login_required(login_url='login')
def game_view(request):
    return render(request, 'tabs/game.html', {})

@login_required(login_url='login')
def stats_view(request):
    
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    obj = Result.objects.filter(Q(player_1__username=username) | Q(player_2__username=username))
    context = {"obj": obj,
               "user": username }
    return render(request, 'tabs/stats.html', context)

@login_required(login_url='login')
def home_view(request):
    return render(request, 'index.html', {})