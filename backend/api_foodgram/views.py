from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import (
    TagSerializer, IngredientSerializer, RecipesWriteSerializer,
    RecipeReadSerializer, FavoriteSerializer
    # CustomUserSerializer,
    # CustomCreateUserSerializer
    )
from .models import Tag, Ingredient, Recipe, Favorite
from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated


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


class RecipesWriteViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipesWriteSerializer
        return RecipeReadSerializer


class CustomUserViewSet(UserViewSet):  # см. по ссылке функционал
# class CustomUserViewSet(viewsets.ModelViewSet): # МНЕ: отложить - пока не разобрался чем наполнять вьюсет
    queryset = User.objects.all()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        recipe = self.kwargs.get('recipe_id')  # 'recipe_id'- это параметр рег.выражения
        return Favorite.objects.filter(recipe_id=recipe)

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe_id=recipe)
