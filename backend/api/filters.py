from django_filters import rest_framework
from recipes.models import Favorite, Recipe, Shopping, Tag


class RecipeFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(
        field_name='name', lookup_expr='icontains')
    author = rest_framework.NumberFilter(field_name='author')
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all())
    is_favorited = rest_framework.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited')
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        return Recipe.objects.filter(
            id__in=Favorite.objects.filter(
                user=self.request.user).values_list('recipe', flat=True))

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return Recipe.objects.filter(
            id__in=Shopping.objects.filter(
                user=self.request.user).values_list('recipe', flat=True))

    class Meta:
        model = Recipe
        fields = [
            'name', 'author', 'is_favorited', 'tags', 'is_in_shopping_cart']
