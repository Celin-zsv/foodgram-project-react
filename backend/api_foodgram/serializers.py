from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, IngredientRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class Ingredient2Serializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def get_amount(self, obj):
        res = IngredientRecipe.objects.filter(ingredient_id=obj.id)
        return res[0].amount


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = Ingredient2Serializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags',)
