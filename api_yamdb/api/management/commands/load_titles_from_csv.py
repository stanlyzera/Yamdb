import csv

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from reviews.models import Categories, Title


class Command(BaseCommand):
    help = 'Load data from reviews.csv into the database'

    def handle(self, *args, **options):
        csv_file_path = 'static/data/titles.csv'

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                try:
                    category = Categories.objects.get(id=row['category'])
                except ObjectDoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            'Category does not exist. Skipping this row.'
                        )
                    )
                    continue
                title = Title(
                    name=row['name'], year=int(row['year']), category=category
                )
                title.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully loaded data from {csv_file_path}')
                )
