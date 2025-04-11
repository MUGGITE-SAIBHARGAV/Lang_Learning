from django.contrib import admin
from .models import Language, Course, Lesson, Exercise, UserProgress

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'level', 'created_at')
    list_filter = ('language', 'level')
    search_fields = ('title', 'description')

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course__language', 'course')
    search_fields = ('title', 'content')
    inlines = [ExerciseInline]

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('question', 'lesson', 'type', 'order')
    list_filter = ('type', 'lesson__course')
    search_fields = ('question', 'answer')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'score', 'last_accessed')
    list_filter = ('completed', 'lesson__course')
    search_fields = ('user__username',)
