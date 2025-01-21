from django.urls import path
from .views import RecipeListView, RecipeDetailView, recipe_search
 
app_name = 'recipes'

urlpatterns = [
   
    path('detail/<pk>/', RecipeDetailView.as_view(), name = 'detail'),
    path('list/', RecipeListView.as_view(), name = 'list'),
    path('search/', recipe_search, name = 'search')
]