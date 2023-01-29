from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


User = get_user_model()


def validate_cooking_time(value):
    if value < 1:
        raise ValidationError(
            'Проверьте время приготовления:'
            ' значение должно быть больше или равно 1')


def validate_amount(value):
    if value < 1:
        raise ValidationError(
            'Проверьте количество: значение должно быть больше или равно 1')


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
        null=True,
        related_name='recipes',
        verbose_name='Автор'
    )
    text = models.TextField('Описание', null=True)
    image = models.ImageField(
        upload_to='images/',
        null=True
    )
    cooking_time = models.IntegerField(
        'Время приготовления (в минутах)',
        validators=[validate_cooking_time]
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', related_name='recipes',
        verbose_name='Список ингредиентов')
    tags = models.ManyToManyField(
        Tag, through='TagRecipe', related_name='recipes',
        verbose_name='Список тегов')

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField(
        'Количество в рецепте', validators=[validate_amount])

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


class Shopping(models.Model):
    recipe_id = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shoppings')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shoppings')

    def __str__(self) -> str:
        return f'{self.recipe_id}.{self.user}'
