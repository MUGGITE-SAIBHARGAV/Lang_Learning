from django.urls import path
from .views import scenario_list, scenario_detail
from django.shortcuts import render
app_name = 'scenarios'  # Namespace for URL resolution

def chat_view(request):
    return render(request, "chat.html")
urlpatterns = [
    path('', scenario_list, name='scenario_list'),
    path('<int:scenario_id>/', scenario_detail, name='scenario_detail'),
    path("chat/", chat_view, name="chat"),
]
