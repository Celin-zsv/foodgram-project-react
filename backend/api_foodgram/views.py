from django.http import HttpResponse
from rest_framework import viewsets, status
from .serializers import (
    TagSerializer, IngredientSerializer, RecipesWriteSerializer,
    RecipeReadSerializer, FavoriteSerializer, ShoppingSerializer,
    SubscriptionSerializer,
    CustomUserSerializer
    # CustomCreateUserSerializer
    )
from .models import (
    Tag, Ingredient, Recipe, Favorite, Shopping, Subscription)
from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
# from djoser.views import UserViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response


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

    @action(methods=['delete', 'post'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_exist = Favorite.objects.filter(
            recipe_id=pk, user=self.request.user)

        if request.method == 'POST':
            if favorite_exist.exists():
                return Response(
                    {'errors': 'Ошибка добавления ДУБЛЯ в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=self.request.user, recipe_id=recipe)
            serializer = FavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':  # Explicit is better than implicit
            if not favorite_exist.exists():
                return Response(
                    {'errors': 'Ошибка удаления: подписка не существует'},
                    status=status.HTTP_400_BAD_REQUEST)
            favorite_exist.delete()
            return Response(
                'Рецепт успешно удален из избранного',
                status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_exist = Shopping.objects.filter(
            recipe_id=recipe, user=self.request.user)

        if request.method == 'POST':
            if shopping_exist.exists():
                return Response(
                    {'error': 'Ошибка добавления ДУБЛЯ в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            Shopping.objects.create(recipe_id=recipe, user=self.request.user)
            serializer = ShoppingSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':   # Explicit is better than implicit
            if not shopping_exist.exists():
                return Response(
                    {'error': 'Ошибка удаления: покупка не существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            shopping_exist.delete()
            return Response(
                'Рецепт успешно удален из списка покупок',
                status=status.HTTP_204_NO_CONTENT
            )


# class CustomUserViewSet(UserViewSet):  # см. по ссылке функционал
# class CustomUserViewSet(viewsets.ModelViewSet): # МНЕ: отложить - пока не разобрался чем наполнять вьюсет

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return SubscriptionSerializer
        return CustomUserSerializer

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk=None):
        following = get_object_or_404(User, pk=pk)  # НА КОГО подписываемся
        subscription_exist = Subscription.objects.filter(
            following_id=following, user=self.request.user)  # КТО подписывается

        if request.method == 'POST':
            if subscription_exist.exists():
                return Response(
                    {'error': 'Ошибка добавления ДУБЛЯ в список подписок на пользователя'},
                    status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(following_id=following, user=self.request.user)
            serializer = SubscriptionSerializer(following)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':   # Explicit is better than implicit
            if not subscription_exist.exists():
                return Response(
                    {'error': 'Ошибка удаления: подписок на пользователя не существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            subscription_exist.delete()
            return Response(
                'Подписка на пользователя успешно удалена из списка подписок',
                status=status.HTTP_204_NO_CONTENT
            )

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset_user = User.objects.filter(
            subscriptions_following__user=self.request.user)
        serializer = self.get_serializer(queryset_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
