from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)
from users.models import User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')
    id = serializers.CharField(source='ingredient.id')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        return User.objects.filter(
            subscriptions_following__following=obj).exists()


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeReadSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'text', 'cooking_time', 'image',)

    def get_is_favorited(self, obj):
        return Favorite.objects.filter(
            user=self.context.get('request').user,
            recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        return Shopping.objects.filter(
            user=self.context.get('request').user,
            recipe=obj).exists()


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeWriteSerializer(
        many=True, allow_empty=False)
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, allow_empty=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags', 'image',)
        read_only_fields = ('author',)

    @staticmethod
    def set_ingredients(recipe, ingredient, ingr_list):
        ingr_list.append(
            IngredientRecipe(
                recipe=recipe,
                ingredient=get_object_or_404(
                    Ingredient, pk=ingredient['id']),
                amount=ingredient['amount']
            )
        )
        return ingr_list

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        ingr_list = list()
        for ingredient in ingredients:
            self.set_ingredients(recipe, ingredient, ingr_list)
        IngredientRecipe.objects.bulk_create(ingr_list)
        recipe.tags.set(tags)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.id = validated_data.get('id', instance.id)
        instance.author = self.context['request'].user

        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            obj_for_del = IngredientRecipe.objects.filter(
                recipe=instance.id)
            ingr_list = list()
            for ingredient in ingredients:
                ingredientrecipe_exist = IngredientRecipe.objects.filter(
                    recipe=instance.id,
                    ingredient=ingredient['id']).exists()
                if ingredientrecipe_exist:
                    obj_for_del = obj_for_del.exclude(
                        ingredient=ingredient['id'])
                    obj_ingredientrecipe = IngredientRecipe.objects.get(
                        recipe=instance.id, ingredient=ingredient['id'])
                    obj_ingredientrecipe.amount = ingredient['amount']
                    obj_ingredientrecipe.save()
                elif not ingredientrecipe_exist:
                    self.set_ingredients(instance, ingredient, ingr_list)
            obj_for_del.delete()
            IngredientRecipe.objects.bulk_create(ingr_list)

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)

        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeReadShortSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data


class RecipeReadShortSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeWriteSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    author = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients',  'name', 'text', 'cooking_time', 'image',)


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time',)


class SubscriptionSerializer(UserSerializer):
    recipes = RecipeShortSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return User.objects.filter(recipes__author=obj.id).count()
