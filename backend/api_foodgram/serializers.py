from django.shortcuts import get_object_or_404
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
        # read_only_fields = ('id',)


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient_id')
    measurement_unit = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def get_measurement_unit(self, obj):
        return obj.ingredient_id.measurement_unit

    def get_id(self, obj):
        return obj.ingredient_id.id


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeReadSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients',  'name', 'text', 'cooking_time', )


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = serializers.CharField(source='ingredients_ref')
    ingredients = IngredientRecipeWriteSerializer(many=True, required=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags',)

    def create(self, validated_data):
        if len(self.initial_data['ingredients']) == 0:
            raise serializers.ValidationError(
                'Обязательный ввод инградиннта-> id')

        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        bulk_list = list()
        for ingredient in ingredients:
            bulk_list.append(
                IngredientRecipe(
                    recipe_id=recipe,
                    ingredient_id=get_object_or_404(
                        Ingredient, pk=ingredient['id']),
                    amount=ingredient['amount']
                )
            )
        IngredientRecipe.objects.bulk_create(bulk_list)
        return recipe

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data
