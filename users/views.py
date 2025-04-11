from django.shortcuts import render
from .models import Profile

def Leaderboard(request):
    top_users= Profile.objects.order_by('-points')[:10]  # Top 10 users
    return render(request, 'users/leaderboard.html', {'top_users': top_users})
