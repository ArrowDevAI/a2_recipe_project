from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart

def Main(request):
    return render(request, 'recipes/home.html')


class RecipeListView(LoginRequiredMixin,ListView):
    model = Recipe
    template_name = "recipes/list.html"

class RecipeDetailView(LoginRequiredMixin,DetailView):                       
    model = Recipe                                        
    template_name = 'recipes/detail.html' 

def recipe_search(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df_html = None
    recipes_df = None
    chart = None
    qs=None
    if request.method == 'POST':
        recipe_title = request.POST.get('recipe_title')
        chart_type = request.POST.get('chart_type')
       
        qs = Recipe.objects.filter(name__icontains=recipe_title)
        if recipe_title == 'all':
                qs = Recipe.objects.all()
        if qs:
            

            recipes_df = pd.DataFrame(qs.values())

            #if there is a 'pic' dataframe column, apply lambda function to each recipe to allow image render
            if 'pic' in recipes_df.columns:
                recipes_df['pic'] = recipes_df['pic'].apply(
                    lambda x: f'<img src="/media/{x}" alt="Recipe Image" style="width:100px;height:auto;">'
                )

            # Initialize ingredients_list
            ingredients_list = []

            # Access related ingredients for each recipe
            for recipe in qs:
                ingredients = recipe.ingredients.all()  # Get related Ingredient objects
                # Get a list of ingredient names
                ingredients_names = [ingredient.name for ingredient in ingredients]
                ingredients_list.append(', '.join(ingredients_names))  # Join names into a comma-separated string

            # Add the ingredients_list as a new column in the DataFrame
            recipes_df['ingredients'] = ingredients_list
            # Reorder columns (if needed)
            # For example, if you want to move the 'ingredients' column right after 'name'
            cols = ['name', 'ingredients', 'difficulty', 'cook_time', 'pic']  # Adjust this as needed
            recipes_df = recipes_df[cols]

            # Convert the DataFrame to an HTML table, and ensure that HTML in 'pic' column is not escaped
            recipes_df_html = recipes_df.to_html(escape=False)

            chart = get_chart(chart_type, recipes_df)
        

    return render(request, 'recipes/results.html', {
        'form': form, 
        'recipes_df': recipes_df_html, 
        'chart': chart,
        'qs': qs
        })