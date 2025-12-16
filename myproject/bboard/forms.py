from django.forms import ModelForm, inlineformset_factory

from .models import Bb, Recipe, Ingredient


class BbForm(ModelForm):
    """Форма для объявления"""
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


class RecipeForm(ModelForm):
    """Форма для рецепта"""
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'image')
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание рецепта',
            'image': 'Изображение рецепта',
        }


class IngredientForm(ModelForm):
    """Форма для ингредиента"""
    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit')
        labels = {
            'name': 'Название ингредиента',
            'quantity': 'Количество',
            'unit': 'Единица измерения',
        }


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=0,
    can_delete=True,
    can_order=False,
)