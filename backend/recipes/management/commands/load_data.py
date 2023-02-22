import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, './', 'ingredients.json')
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            model_class = Ingredient
            load_list = []
            v_max_id = model_class.objects.order_by('-id').first().id + 1
            for i in data:
                if not model_class.objects.filter(name=i['name']).exists():
                    item_ingredient = model_class()
                    item_ingredient.pk = v_max_id
                    item_ingredient.name = i['name']
                    item_ingredient.measurement_unit = i['measurement_unit']

                    load_list.append(item_ingredient)
                    v_max_id += 1
            Ingredient.objects.bulk_create(load_list)

        print(
            f'loaded {len(load_list)} rec from JSON in {model_class.__name__}')
