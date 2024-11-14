import csv
import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Convert a CSV file to JSON format for importing into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        json_file = options['json_file']

        data = []
        with open(csv_file, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({
                    'model': 'tasks.tasktemplate',
                    'pk': int(row['pk']),
                    'fields': {
                        'task_type': row['task_type'],
                        'day_of_culture': int(row['day_of_culture'])
                    }
                })

        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'CSV data has been successfully converted to {json_file}'))

