from django.conf import settings
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование', max_length=settings.MAX_LENGTH_NAME, db_index=True)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=settings.MAX_LENGTH_NAME)

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Наименование', max_length=settings.MAX_LENGTH_NAME, db_index=True)
    color = models.CharField(
        'Цвет в HEX', max_length=7, null=False,
        validators=[RegexValidator('^#([A-Fa-f0-9]{3,6})$', message=(
            'Ошибка ввода Hex'))])
    slug = models.SlugField('Слаг', max_length=200, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['slug'], name='unique_slug')]


class Recipe(models.Model):
    name = models.CharField(
        'Наименование', max_length=settings.MAX_LENGTH_NAME, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField('Описание', null=True)
    image = models.ImageField(
        upload_to='recipes/images/', null=True, default=None)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (в минутах)', validators=[MinValueValidator(1)]
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список тегов')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-pub_date']


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='+')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.PositiveSmallIntegerField(
        'Количество в рецепте', validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.ingredient}.{self.recipe}.{self.amount}'

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe')]


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self) -> str:
        return f'{self.recipe}.{self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_user'
            )
        ]


class Shopping(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoppings')

    def __str__(self) -> str:
        return f'{self.recipe}.{self.user}'
