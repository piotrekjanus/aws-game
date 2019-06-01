from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Result
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime
import json
from django.contrib.auth.models import User


@login_required(login_url='login')
def game_view(request):
    return render(request, 'tabs/game.html', {})


@login_required(login_url='login')
def stats_view(request):
    username = None
    context = {}
    if request.user.is_authenticated:
        username = request.user.username
        obj = Result.objects.filter(Q(player_1__username=username) | Q(player_2__username=username))
        context = {"obj": obj,
                   "user": username}
    return render(request, 'tabs/stats.html', context)


@login_required(login_url='login')
def home_view(request):
    return render(request, 'index.html', {})


@csrf_exempt
def get_match_result(request):
    if request.POST:
        status = request.POST.getlist('info')[0]
        users = json.loads(request.POST.getlist('users')[0])
        if request.user.is_authenticated:
            user_name = request.user.username
        result = Result()
        result.date = datetime.datetime.utcnow()
        result.player_1 = User.objects.get(username=users[0])
        result.player_2 = User.objects.get(username=users[1])
        if(status == 'winner'):
            result.winner = User.objects.get(username=user_name)
            result.save()
        # return render(request, 'index.html', {})
    elif request.GET:
        return HttpResponse()
    else:
        return HttpResponse()
