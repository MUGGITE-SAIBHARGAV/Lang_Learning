from django.urls import path
from .views import Leaderboard

app_name = 'users' 

urlpatterns = [
    path('leaderboard/', Leaderboard, name='leaderboard'),
]
