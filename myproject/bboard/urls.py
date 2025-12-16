from django.urls import path

from .views import (
    index, rubric_bbs, BbCreateView,
    RecipeListView, RecipeDetailView,
    recipe_create, recipe_update, recipe_delete
)

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', rubric_bbs, name='rubric_bbs'),
    path('', index, name='index'),
    # URL для рецептов
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/create/', recipe_create, name='recipe_create'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/<int:pk>/update/', recipe_update, name='recipe_update'),
    path('recipes/<int:pk>/delete/', recipe_delete, name='recipe_delete'),
]