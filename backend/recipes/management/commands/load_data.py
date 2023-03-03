import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, './', 'ingredients.json')
        try:
            with open(path, encoding='utf-8') as upload_file:
                data = json.load(upload_file)
                load_list = []
                for i in data:
                    if not Ingredient.objects.filter(name=i['name']).exists():
                        item_ingredient = Ingredient()
                        item_ingredient.name = i['name']
                        item_ingredient.measurement_unit = i[
                            'measurement_unit']

                        load_list.append(item_ingredient)
                Ingredient.objects.bulk_create(load_list)
        except IOError as err:
            print(f'Error with file open:: {err}')

        print(
            f'loaded {len(load_list)} rec from JSON in {Ingredient.__name__}')
