from django.contrib import admin
from .models import Scenario, Dialogue

class DialogueInline(admin.TabularInline):
    model = Dialogue
    extra = 1  # Allows adding dialogues directly in the Scenario admin

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')  # Displayed columns in admin list
    search_fields = ('title', 'category')
    list_filter = ('category',)
    inlines = [DialogueInline]  # Allows adding dialogues inside Scenario admin

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('scenario', 'speaker', 'text', 'order')
    list_filter = ('scenario',)
    ordering = ('scenario', 'order')
