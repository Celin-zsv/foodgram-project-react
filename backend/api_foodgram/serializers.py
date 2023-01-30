from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, IngredientRecipe


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        # fields = ('id', 'name', 'measurement_unit',)
        fields = ('id', 'name', 'measurement_unit', 'amount')
        # read_only_fields = ('id',)

    def get_amount(self, obj):
        return 1


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


# post: add resepe
class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'author', 'text',
            'cooking_time', 'ingredients', 'tags',)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        print(f'ingredients_BEFORE:{ingredients} BEFORE!!')
        var_context = self.context['request'].data
        print(f'self.context:  {var_context}   BEFORE!!')
        var_ini = self.initial_data['ingredients'][0]['amount']
        print(f'initial_data:  {var_ini}   initial_data')

        recipe = Recipe.objects.create(**validated_data)
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            print(f'ingredient123:{ingredient} !!')
            var_len = len(ingredient['name'])
            print(f'LEN_ingredient123:{var_len} !!')
            IngredientRecipe.objects.create(
                ingredient_id=current_ingredient,
                recipe_id=recipe,
                # amount=validated_data.amount
                # amount='448'
                # amount=ingredient['name']
                amount=var_len
                # amount=status
            )

        return recipe


# class IngredientRecipeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = IngredientRecipe
#         fields = ('id', 'ingredient_id', 'recipe_id', 'amount',)
#         # fields = ('id', 'amount',)


# # post: add resepe-2
# class RecipesSerializer(serializers.ModelSerializer):
#     ingredients = IngredientSerializer(many=True)
#     tags = TagSerializer(read_only=True, many=True)

#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'name', 'author', 'text',
#             'cooking_time', 'ingredients', 'tags',)

#     def create(self, validated_data):
#         print(f'validated_data_BEFORE:  {validated_data}  BEFORE!!')
#         ingredients = validated_data.pop('ingredients')
#         print(f'validated_data_AFTER:  {validated_data}  AFTER!!')
#         print(f'ingredients_BEFORE-1:{ingredients} BEFORE-1!!')
#         ingredients2 = dict(ingredients)
#         print(f'ingredients2_BEFORE-2:{ingredients2} BEFORE-2!!')

#         # var_context = self.context['request'].data
#         # print(f'self.context:  {var_context}   BEFORE!!')

#         recipe = Recipe.objects.create(**validated_data)
#         for ingredient in ingredients:
#             current_ingredient, status = Ingredient.objects.get_or_create(
#                 **ingredient
#             )
#             # current_ingredient = Ingredient.objects.get(
#             #     **ingredient
#             # )
#             print(f'current_ingredient:  {current_ingredient}  !!')
#             # IngredientRecipe.objects.create(recipe_id=recipe, **ingredient)
#             print(f'ingredient123:{ingredient} !!')
#             var_len = len(ingredient['name'])
#             print(f'LEN_ingredient123:{var_len} !!')
#             IngredientRecipe.objects.create(
#                 ingredient_id=current_ingredient,
#                 recipe_id=recipe,
#                 # amount=validated_data.amount
#                 # amount='448'
#                 # amount=ingredient['name']
#                 amount=var_len
#                 # amount=recipe.
#             )

#         return recipe


# # post: add resepe-3
# class RecipesSerializer(serializers.ModelSerializer):
#     ingredients = IngredientSerializer(many=True)
#     tags = TagSerializer(read_only=True, many=True)

#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'name', 'author', 'text',
#             'cooking_time', 'ingredients', 'tags',)

#     def create(self, validated_data):
#         ingredients = validated_data.pop('ingredients')

#         recipe = Recipe.objects.create(**validated_data)
#         for ingredient in ingredients:
#             current_ingredient, status = Ingredient.objects.get_or_create(
#                 **ingredient
#             )
#             IngredientRecipe.objects.create(
#                 ingredient_id=current_ingredient,
#                 recipe_id=recipe,
#                 # amount=validated_data.amount
#                 # amount='448'
#                 # amount=ingredient['name']
#                 amount=55
#                 # amount=status
#             )

#         return recipe
