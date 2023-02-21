import io

from django.http import FileResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
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
            return Recipe.objects.filter(favorites__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart'):
            return Recipe.objects.filter(shoppings__user=self.request.user)
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
            recipe_id=pk, user=self.request.user)

        if request.method == 'POST':
            if favorite_exist.exists():
                return Response(
                    {'errors': 'Ошибка добавления ДУБЛЯ в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=self.request.user, recipe_id=recipe)
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
            recipe_id=recipe, user=self.request.user)

        if request.method == 'POST':
            if shopping_exist.exists():
                return Response(
                    {'error': 'Ошибка добавления ДУБЛЯ в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            Shopping.objects.create(recipe_id=recipe, user=self.request.user)
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
        recepes = Recipe.objects.filter(
            shoppings__user=self.request.user)
        ingredients = Ingredient.objects.filter(
            recipes__shoppings__user=self.request.user)
        ingredientrecipes = IngredientRecipe.objects.filter(
            ingredient_id__in=ingredients, recipe_id__in=recepes)
        return getpdf(ingredientrecipes)


class APISubscribePostDelete(mixins.CreateModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, **kwargs):

        following = get_object_or_404(User, pk=kwargs['user_id'])  # on whom
        subscription_exist = Subscription.objects.filter(
            following_id=following, user=self.request.user)  # who

        if subscription_exist.exists():
            return Response(
                {'error': 'Ошибка добавления ДУБЛЯ в список подписок'},
                status=status.HTTP_400_BAD_REQUEST)
        if following == self.request.user:
            return Response(
                {'error': 'Ошибка добавления подписки НА СЕБЯ'},
                status=status.HTTP_400_BAD_REQUEST)

        Subscription.objects.create(
            following_id=following, user=self.request.user)
        serializer = SubscriptionSerializer(following)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, **kwargs):
        following = get_object_or_404(User, pk=kwargs['user_id'])  # on whom
        subscription_exist = Subscription.objects.filter(
            following_id=following, user=self.request.user)  # who

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


def getpdf(ingredients):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textobj = c.beginText()
    textobj.setTextOrigin(inch, 1 * inch)
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    textobj.setFont('Arial', 12)

    lines = []
    for ingr in ingredients:
        if ingr.ingredient_id.name in lines:
            nam_index = lines.index(ingr.ingredient_id.name)
            lines[nam_index + 1] = str(int(lines[nam_index + 1]) + ingr.amount)
        if ingr.ingredient_id.name not in lines:
            lines.append(f'{ingr.ingredient_id.name}')
            lines.append(f'{ingr.amount}')
            lines.append(f'{ingr.ingredient_id.measurement_unit}')

    x = 144
    y = 14
    textobj.moveCursor(x, 0)
    textobj.textOut('Список покупок')
    textobj.moveCursor(-x, 0)
    textobj.textLine()
    textobj.textLine()
    v_count = 2
    for line in lines:
        textobj.textOut(line)
        if v_count == 0:
            v_count = 3
            textobj.moveCursor(-x * 2, y)
        else:
            textobj.moveCursor(x, 0)
        v_count -= 1

    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='shopping_list.pdf')
