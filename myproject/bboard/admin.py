from django.contrib import admin

from .models import Bb, Rubric, Recipe, Ingredient


class BbAdmin(admin.ModelAdmin):
    """Админка для объявлений"""
    list_display = ('rubric', 'title', 'content', 'price', 'published')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content')


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'ingredient_count')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    inlines = [IngredientInline]

    def ingredient_count(self, obj):

        return obj.ingredients.count()
    ingredient_count.short_description = 'Количество ингредиентов'


admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
