 
import json
from django.core.management.base import BaseCommand
from scenarios.models import Scenario, Dialogue  # ✅ change 'scenarios' if your app name is different

class Command(BaseCommand):
    help = 'Import multiple scenarios and dialogues from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['json_file']
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for scenario_data in data['scenarios']:
            scenario = Scenario.objects.create(
                title=scenario_data['title'],
                category=scenario_data.get('category', ''),
                description=scenario_data.get('description', ''),
                image=scenario_data.get('image', 'scenarios/default.png')
            )

            for dialogue in scenario_data['dialogues']:
                Dialogue.objects.create(
                    scenario=scenario,
                    speaker=dialogue['speaker'],
                    text=dialogue['text'],
                    order=dialogue['order']
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Imported: {scenario.title}"))

        self.stdout.write(self.style.SUCCESS("🎉 All scenarios imported successfully."))
