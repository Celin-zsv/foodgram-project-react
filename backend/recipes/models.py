from django.core.validators import MinValueValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        'Наименование', max_length=200, db_index=True, null=False)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=200, null=False
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Наименование', max_length=200, db_index=True, null=False)
    color = models.CharField('Цвет в HEX', max_length=7, null=False)
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
        'Наименование', max_length=200, db_index=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField('Описание', null=True)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[MinValueValidator(1)]
    )
    ingredients_ref = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', related_name='recipes',
        verbose_name='Список ингредиентов')
    tags = models.ManyToManyField(
        Tag, through='TagRecipe', related_name='recipes',
        verbose_name='Список тегов')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-pub_date']


class IngredientRecipe(models.Model):
    ingredient_id = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingradientrecipes')
    recipe_id = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='ingredients')
    amount = models.IntegerField(
        'Количество в рецепте', validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.ingredient_id}.{self.recipe_id}.{self.amount}'

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient_id', 'recipe_id'],
                name='unique_ingredient_recipe')]


class TagRecipe(models.Model):
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.tag_id}.{self.recipe_id}'


class Favorite(models.Model):
    recipe_id = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self) -> str:
        return f'{self.recipe_id}.{self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe_id', 'user'],
                name='unique_recipe_user'
            )
        ]


class Shopping(models.Model):
    recipe_id = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shoppings')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoppings')

    def __str__(self) -> str:
        return f'{self.recipe_id}.{self.user}'