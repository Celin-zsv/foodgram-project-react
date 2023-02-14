import base64

import webcolors
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User

from recipes.models import (
    Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe)
from users.models import Subscription


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

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


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        if not self.context:
            return User.objects.filter(
                subscriptions_following__following_id=obj).exists()
        return Subscription.objects.filter(
            user=self.context.get('request').user,
            following_id=obj).exists()


class RecipeReadSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeReadSerializer(many=True, read_only=True)
    image = Base64ImageField(required=False, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(many=False, read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author',
            'ingredients',  'name', 'text', 'cooking_time', 'image',)


class RecipesWriteSerializer(serializers.ModelSerializer):
    ingredients = serializers.CharField(source='ingredients_ref')
    ingredients = IngredientRecipeWriteSerializer(
        many=True, required=True, allow_empty=False)
    image = Base64ImageField(required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, allow_empty=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags', 'image',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
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

        bulk_list = list()
        for tag in tags:
            bulk_list.append(
                TagRecipe(
                    recipe_id=recipe,
                    tag_id=get_object_or_404(
                        Tag, pk=tag.id)
                )
            )
        TagRecipe.objects.bulk_create(bulk_list)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.text)
        instance.image = validated_data.get('image', instance.image)
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

        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            obj_for_del = TagRecipe.objects.filter(
                recipe_id=instance.id)
            bulk_list = list()
            for tag in tags:
                tagrecipe_exist = TagRecipe.objects.filter(
                    recipe_id=instance.id,
                    tag_id=tag.id).exists()
                if tagrecipe_exist:
                    obj_for_del = obj_for_del.exclude(
                        tag_id=tag.id)
                    obj_tagrecipe = TagRecipe.objects.get(
                        recipe_id=instance.id, tag_id=tag.id)
                    obj_tagrecipe.save()
                elif not tagrecipe_exist:
                    bulk_list.append(
                        TagRecipe(
                            recipe_id=instance,
                            tag_id=get_object_or_404(
                                Tag, pk=tag.id)
                        )
                    )
            obj_for_del.delete()
            TagRecipe.objects.bulk_create(bulk_list)

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
    author = CustomUserSerializer(many=False, read_only=True)

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


class SubscriptionSerializer(CustomUserSerializer):
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
