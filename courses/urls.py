from django.urls import path
from . import views 

app_name = 'courses'

urlpatterns = [
    path('', views.home, name='home'),
    path('languages/', views.language_list, name='language_list'),
    path('courses/<int:language_id>/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('submit-exercise/<int:exercise_id>/', views.submit_exercise, name='submit_exercise'),
    path('profile/', views.user_profile, name='user_profile'),

   
] 