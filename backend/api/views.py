from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)
from users.models import Subscription, User

from .serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipesWriteSerializer,
                          SubscriptionSerializer, TagSerializer)
from .utils import getpdf


def zsv_page(request):
    return HttpResponse('ЭТО zsv page!')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)
    pagination_class = None


class RecipesWriteViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.query_params.get('is_favorited'):
            return Recipe.objects.filter(
                id__in=Favorite.objects.filter(
                    user=self.request.user).values_list('recipe', flat=True)
                    )

        if self.request.query_params.get('is_in_shopping_cart'):
            return Recipe.objects.filter(
                id__in=Shopping.objects.filter(
                    user=self.request.user).values_list('recipe', flat=True)
                    )
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipesWriteSerializer
        return RecipeReadSerializer

    @action(methods=['delete', 'post'], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_exist = Favorite.objects.filter(
            recipe=pk, user=self.request.user)

        if request.method == 'POST':
            if favorite_exist.exists():
                return Response(
                    {'errors': 'Ошибка добавления ДУБЛЯ в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=self.request.user, recipe=recipe)
            serializer = RecipeShortSerializer(recipe)
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
            recipe=recipe, user=self.request.user)

        if request.method == 'POST':
            if shopping_exist.exists():
                return Response(
                    {'error': 'Ошибка добавления ДУБЛЯ в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            Shopping.objects.create(recipe=recipe, user=self.request.user)
            serializer = RecipeShortSerializer(recipe)
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

    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        ingredientrecipes = IngredientRecipe.objects.filter(
            recipe__in=Recipe.objects.filter(
                id__in=Shopping.objects.filter(
                    user=self.request.user).values_list('recipe', flat=True)
                    ))
        return getpdf(ingredientrecipes)


class APISubscribePostDelete(mixins.CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, **kwargs):

        following = get_object_or_404(User, pk=kwargs['user_id'])  # on whom
        subscription_exist = Subscription.objects.filter(
            following=following, user=self.request.user)  # who

        if subscription_exist.exists():
            return Response(
                {'error': 'Ошибка добавления ДУБЛЯ в список подписок'},
                status=status.HTTP_400_BAD_REQUEST)
        if following == self.request.user:
            return Response(
                {'error': 'Ошибка добавления подписки НА СЕБЯ'},
                status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.create(
            following=following, user=self.request.user)
        serializer = SubscriptionSerializer(following)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        following = get_object_or_404(User, pk=kwargs['user_id'])  # on whom
        subscription_exist = Subscription.objects.filter(
            following=following, user=self.request.user)  # who

        if not subscription_exist.exists():
            return Response(
                {'error': 'Ошибка удаления: подписок on user не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription_exist.delete()

        return Response(
            'Подписка на пользователя успешно удалена из списка подписок',
            status=status.HTTP_204_NO_CONTENT
        )


class APISubscriptionsList(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = User.objects.filter(
                subscriptions_following__user=self.request.user)
        return queryset
