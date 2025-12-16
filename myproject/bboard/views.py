from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.forms import inlineformset_factory
from django.urls import reverse_lazy

from .forms import BbForm, RecipeForm, IngredientForm
from .models import Bb, Rubric, Recipe, Ingredient

def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)

def rubric_bbs(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/rubric_bbs.html', context)

class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    success_url = '/bboard/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class RecipeListView(ListView):
    """Список всех рецептов"""
    model = Recipe
    template_name = 'bboard/recipe_list.html'
    context_object_name = 'recipes'
    ordering = ['-created_at']


class RecipeDetailView(DetailView):
    """Детальный просмотр рецепта"""
    model = Recipe
    template_name = 'bboard/recipe_detail.html'
    context_object_name = 'recipe'

def _create_ingredient_formset(extra=0):
    """Создает formset для ингредиентов"""
    return inlineformset_factory(
        Recipe,
        Ingredient,
        form=IngredientForm,
        extra=extra,
        can_delete=True,
        can_order=False
    )


def recipe_create(request):
    """Создание нового рецепта с ингредиентами"""
    extra_forms = int(request.GET.get('extra', 1))

    if request.method == 'POST':
        if 'add_ingredient' in request.POST:
            form = RecipeForm(request.POST, request.FILES)
            total_forms = int(request.POST.get('ingredients-TOTAL_FORMS', 0))
            new_extra = extra_forms + 1

            IngredientFormSet = _create_ingredient_formset(extra=new_extra)
            post_data = request.POST.copy()
            new_total = total_forms + 1
            post_data['ingredients-TOTAL_FORMS'] = str(new_total)
            post_data[f'ingredients-{total_forms}-name'] = ''
            post_data[f'ingredients-{total_forms}-quantity'] = ''
            post_data[f'ingredients-{total_forms}-unit'] = 'г'
            formset = IngredientFormSet(post_data)
            extra_forms = new_extra
        else:
            form = RecipeForm(request.POST, request.FILES)
            IngredientFormSet = _create_ingredient_formset(extra=extra_forms)
            formset = IngredientFormSet(request.POST)

            if form.is_valid() and formset.is_valid():
                recipe = form.save()
                formset.instance = recipe
                formset.save()
                return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        IngredientFormSet = _create_ingredient_formset(extra=extra_forms)
        formset = IngredientFormSet()

    return render(request, 'bboard/recipe_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Создать рецепт',
        'extra_forms': extra_forms
    })

def recipe_update(request, pk):
    """Редактирование рецепта с ингредиентами"""
    recipe = get_object_or_404(Recipe, pk=pk)
    extra_forms = int(request.GET.get('extra', 0))

    if request.method == 'POST':
        if 'add_ingredient' in request.POST:
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            total_forms = int(request.POST.get('ingredients-TOTAL_FORMS', 0))
            new_extra = extra_forms + 1

            IngredientFormSet = _create_ingredient_formset(extra=new_extra)
            post_data = request.POST.copy()
            new_total = total_forms + 1
            post_data['ingredients-TOTAL_FORMS'] = str(new_total)
            post_data[f'ingredients-{total_forms}-name'] = ''
            post_data[f'ingredients-{total_forms}-quantity'] = ''
            post_data[f'ingredients-{total_forms}-unit'] = 'г'
            formset = IngredientFormSet(post_data, instance=recipe)
            extra_forms = new_extra
        else:
            form = RecipeForm(request.POST, request.FILES, instance=recipe)
            IngredientFormSet = _create_ingredient_formset(extra=extra_forms)
            formset = IngredientFormSet(request.POST, instance=recipe)

            if form.is_valid() and formset.is_valid():
                recipe = form.save()
                formset.save()
                return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        IngredientFormSet = _create_ingredient_formset(extra=extra_forms)
        formset = IngredientFormSet(instance=recipe)

    return render(request, 'bboard/recipe_form.html', {
        'form': form,
        'formset': formset,
        'recipe': recipe,
        'title': 'Редактировать рецепт',
        'extra_forms': extra_forms
    })

def recipe_delete(request, pk):
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'bboard/recipe_confirm_delete.html', {'recipe': recipe})