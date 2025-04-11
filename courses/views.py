from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Language, Course, Lesson, Exercise, UserProgress
import json

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from users.models import Profile

def home(request):
    languages = Language.objects.all()
    return render(request, 'courses/home.html', {'languages': languages})

def language_list(request):
    languages = Language.objects.all()
    return render(request, 'courses/language_list.html', {'languages': languages})

def course_list(request, language_id):
    language = get_object_or_404(Language, id=language_id)
    courses = Course.objects.filter(language=language)
    return render(request, 'courses/course_list.html', {
        'language': language,
        'courses': courses
    })
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all()
    
    # Get user progress if logged in
    user_progress = {}
    if request.user.is_authenticated:
        progress_objects = UserProgress.objects.filter(
            user=request.user,
            lesson__course=course
        )
        for progress in progress_objects:
            user_progress[progress.lesson.id] = progress
    
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'user_progress': user_progress
    })

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Get or create user progress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=lesson,
        defaults={'completed': False, 'score': 0}
    )
    
    # Mark as accessed
    progress.save()
    
    return render(request, 'courses/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress
    })

@login_required
def exercise_detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    
    return render(request, 'courses/exercise_detail.html', {
        'exercise': exercise
    })

@login_required
def submit_exercise(request, exercise_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    user_answer = request.POST.get('answer', '')
    
    # Check if correct
    is_correct = False
    if exercise.type == 'multiple_choice':
        is_correct = user_answer == exercise.answer
    elif exercise.type == 'fill_blank' or exercise.type == 'translation':
        # Case insensitive and strip whitespace for text answers
        is_correct = user_answer.strip().lower() == exercise.answer.strip().lower()
    elif exercise.type == 'matching':
        # For matching, compare JSON objects
        try:
            user_matches = json.loads(user_answer)
            correct_matches = json.loads(exercise.answer)
            is_correct = user_matches == correct_matches
        except json.JSONDecodeError:
            is_correct = False
    
    # Update progress
    progress, created = UserProgress.objects.get_or_create(
        user=request.user,
        lesson=exercise.lesson,
        defaults={'completed': False, 'score': 0}
    )
    
    if is_correct:
        progress.score += exercise.points
        progress.save()
    
    # Check if this was the last exercise in the lesson
    last_exercise = exercise.lesson.exercises.order_by('-order').first()
    if exercise.id == last_exercise.id:
        progress.completed = True
        progress.save()
    
    return JsonResponse({
        'is_correct': is_correct,
        'correct_answer': exercise.answer,
        'score': progress.score,
        'completed': progress.completed
    })

@login_required
def user_profile(request):
    progress_list = UserProgress.objects.filter(user=request.user)
    
    # Group by course
    courses_progress = {}
    total_score = 0
    completed_lessons = 0
    
    for progress in progress_list:
        course_id = progress.lesson.course.id
        if course_id not in courses_progress:
            courses_progress[course_id] = {
                'course': progress.lesson.course,
                'lessons_completed': 0,
                'total_lessons': progress.lesson.course.lessons.count(),
                'score': 0
            }
        
        if progress.completed:
            courses_progress[course_id]['lessons_completed'] += 1
            completed_lessons += 1
        
        courses_progress[course_id]['score'] += progress.score
        total_score += progress.score
    
    return render(request, 'courses/user_profile.html', {
        'courses_progress': courses_progress.values(),
        'total_score': total_score,
        'completed_lessons': completed_lessons
    })
