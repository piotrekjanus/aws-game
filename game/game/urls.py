from django.contrib import admin
from django.urls import path, include
from login.views import register_view, login_view, logout_view
from tabs.views import home_view, game_view, stats_view, get_match_result

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('game/', game_view, name='game'),
    path('stats/', stats_view, name='stats'),
    path('home/', home_view, name='homepage'),
    path('admin/', admin.site.urls),
    path('results/', get_match_result, name='results')
]
