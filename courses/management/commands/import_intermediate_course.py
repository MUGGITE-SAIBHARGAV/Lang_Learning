import json
from django.core.management.base import BaseCommand
from courses.models import Course, Lesson, Exercise, Language  # ✅ Import Language model

class Command(BaseCommand):
    help = 'Import intermediate course with lessons and exercises from JSON'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to intermediate.json')

    def handle(self, *args, **kwargs):
        file_path = kwargs['json_file']
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # ✅ Get or create the Language
        language_name = data.get('language', 'English')  # or pass it in JSON
        language, created = Language.objects.get_or_create(name=language_name)

        # ✅ Create the course with language
        course = Course.objects.create(
            title=data['course_title'],
            level=data['level'],
            language=language  # this is the required field
        )

        for i, lesson_data in enumerate(data['lessons'], start=1):
            lesson = Lesson.objects.create(
              course=course,
              title=lesson_data['title'],
              content=lesson_data['content'],
              order=i  # ✅ fixed: provides lesson order automatically
    )

            for i, ex in enumerate(lesson_data['exercises'], start=1):
                Exercise.objects.create(
                    lesson=lesson,
                    type=ex['type'],
                    question=ex['question'],
                    options=ex.get('options'),
                    answer=ex.get('answer', ''),
                    pairs=ex.get('pairs'),
                    order=i
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Imported: {lesson.title}"))

        self.stdout.write(self.style.SUCCESS("🎉 Intermediate course imported successfully!"))
    