from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.models import (
    Ingredient, Tag, Recipe, IngredientRecipe, TagRecipe, Favorite, Shopping)
    # Subscription)
# from users.models import User


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'cooking_time')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe_id', 'user')


# @admin.register(User)
# class CustomUser(UserAdmin):
#     list_filter = ('email', 'username')


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(TagRecipe)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping)
# admin.site.register(Subscription)
