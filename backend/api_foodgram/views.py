from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from.serializers import TagSerializer, IngredientSerializer
from .models import Tag, Ingredient
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
