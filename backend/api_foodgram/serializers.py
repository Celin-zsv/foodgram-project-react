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
    ingredients = IngredientRecipeWriteSerializer(
        many=True, required=True, allow_empty=False)
    tags = TagSerializer(read_only=True, many=True, allow_empty=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags',)

    def create(self, validated_data):
        if 'ingredients' not in self.initial_data:
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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.text)
        instance.id = validated_data.get('id', instance.id)
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            obj_for_del = IngredientRecipe.objects.filter(
                recipe_id=instance.id)

            bulk_list = list()
            for ingredient in ingredients:
                ingredientrecipe_exist = IngredientRecipe.objects.filter(
                    recipe_id=instance.id,
                    ingredient_id=ingredient['id']).exists()
                if ingredientrecipe_exist:
                    obj_for_del = obj_for_del.exclude(
                        ingredient_id=ingredient['id'])
                    obj_ingredientrecipe = IngredientRecipe.objects.get(
                        recipe_id=instance.id, ingredient_id=ingredient['id'])
                    obj_ingredientrecipe.amount = ingredient['amount']
                    obj_ingredientrecipe.save()
                elif not ingredientrecipe_exist:
                    bulk_list.append(
                        IngredientRecipe(
                            recipe_id=instance,
                            ingredient_id=get_object_or_404(
                                Ingredient, pk=ingredient['id']),
                            amount=ingredient['amount']
                        )
                    )

            obj_for_del.delete()
            IngredientRecipe.objects.bulk_create(bulk_list)
        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data
