from django import forms
from django.contrib import admin
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Shopping, Tag)


class RequiredFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False


class IngredientRecipeAdmin(admin.TabularInline):
    model = IngredientRecipe
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    extra = 3
    show_change_link = True
    formset = RequiredFormSet
    max_num = 33


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'text', 'cooking_time')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('name', 'author', 'tags', 'pub_date')
    filter_vertical = ('tags',)
    inlines = [
        IngredientRecipeAdmin,
    ]


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Shopping)
