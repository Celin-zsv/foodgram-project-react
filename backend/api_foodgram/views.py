from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, RecipesSerializer)
from .models import Tag, Ingredient, Recipe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


def zsv_page(request):
    return HttpResponse('ЭТО zsv page!')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
    # search_fields = ('$name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer
