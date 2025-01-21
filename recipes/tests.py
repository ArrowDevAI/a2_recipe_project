from django.test import TestCase
from .models import Recipe
from ingredients.models import Ingredient
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import RecipeSearchForm



class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
    #Add ingredients to the test database for testing
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.ingredient1 = Ingredient.objects.create(name="Butter")
        cls.ingredient2 = Ingredient.objects.create(name="Bread")
        cls.ingredient3 = Ingredient.objects.create(name="Cheese")
        cls.ingredient4 = Ingredient.objects.create(name="Salt")
        cls.ingredient5 = Ingredient.objects.create(name="Pepper")
        cls.easy_recipe = Recipe.objects.create(name='Easy Recipe', cook_time=5)
        cls.easy_recipe.ingredients.add(cls.ingredient1, cls.ingredient2)
        
        cls.medium_recipe = Recipe.objects.create(name='Medium Recipe', cook_time=5)
        cls.medium_recipe.ingredients.add(cls.ingredient1, cls.ingredient2, cls.ingredient3, cls.ingredient4, cls.ingredient5)
        
        cls.intermediate_recipe = Recipe.objects.create(name='Intermediate Recipe', cook_time=15)
        cls.intermediate_recipe.ingredients.add(cls.ingredient1)
        
        cls.hard_recipe = Recipe.objects.create(name='Hard Recipe', cook_time=15)
        cls.hard_recipe.ingredients.add(cls.ingredient1, cls.ingredient2, cls.ingredient3, cls.ingredient4, cls.ingredient5)

        cls.test_recipe = Recipe.objects.create(
            name = 'Grilled Cheese',
            cook_time = 5,
        )
        cls.test_recipe.ingredients.add(cls.ingredient1, cls.ingredient2)
    
    def test_database_entry(self):
        recipe = self.medium_recipe
        difficulty = recipe.calc_difficulty()
        self.assertEqual(recipe.name, 'Medium Recipe')
        self.assertEqual(recipe.cook_time, 5)
        self.assertEqual(recipe.ingredients.count(), 5)
        self.assertEqual(recipe.difficulty, 'Medium')

    def test_recipe_name(self):
        test_recipe = Recipe.objects.get(name='Grilled Cheese')
        field_label = test_recipe._meta.get_field('name').verbose_name
        self.assertEqual(test_recipe.name, 'Grilled Cheese')
        self.assertEqual(field_label, 'name')
       
    def test_ingredient_name(self):
        test_recipe = self.test_recipe
        field_label = test_recipe._meta.get_field('ingredients').verbose_name
        self.assertEqual(field_label,'ingredients')
        self.assertEqual(test_recipe.ingredients.count(), 2)
    
    def test_difficulty_name(self):
        test_recipe = self.test_recipe
        field_label = test_recipe._meta.get_field('difficulty').verbose_name
        self.assertEqual(field_label, "difficulty")
    def test_calc_difficulty(self):
        recipes_with_expected_difficulties = [
            (self.easy_recipe, "Easy"),
            (self.medium_recipe, "Medium"),
            (self.intermediate_recipe, "Intermediate"),
            (self.hard_recipe, "Hard"),
        ]

        for recipe, expected_difficulty in recipes_with_expected_difficulties:
            recipe.calc_difficulty()
            self.assertEqual(recipe.difficulty, expected_difficulty)

    def test_str_method(self):
        recipe = self.medium_recipe 
        expected_str = f"Name: {recipe.name} | Cook Time: {recipe.cook_time} mins | " \
                       f"Difficulty: {recipe.difficulty} | Ingredients: {recipe.ingredients.count()}"
        self.assertEqual(str(recipe), expected_str)
    
    def test_get_absolute_url(self):
        recipe = Recipe.objects.first()
        self.assertIsNotNone(recipe, "No book instances exist to test get_absolute_url.")
        self.assertEqual(recipe.get_absolute_url(), f'/recipes/detail/{recipe.id}/')
    
    def test_main_view_template(self):
        response = self.client.get(reverse('recipes:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/home.html')

    def test_recipe_list_view_template(self):
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('recipes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/list.html')

    def test_recipe_detail_view_template(self):
        self.client.login(username=self.user.username, password='password')
        recipe = Recipe.objects.first()
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')

class RecipeSearchFormTest(TestCase):
    def setUp(self):
        self.default_data = {
            'recipe_title': 'Test Recipe',
            'chart_type': '#1'
        }

    def test_form_valid_data(self):
        form = RecipeSearchForm(data=self.default_data)
        self.assertTrue(form.is_valid())

    def test_invalid_recipe_title(self):
        form = RecipeSearchForm(data={**self.default_data, 'recipe_title': ''})
        self.assertFalse(form.is_valid())

    def test_invalid_chart_type(self):
        form = RecipeSearchForm(data={**self.default_data, 'chart_type': ''})
        self.assertFalse(form.is_valid())
    
    def test_invalid_recipe_title(self):
        form = RecipeSearchForm(data={**self.default_data, 'recipe_title': ''})
        self.assertFalse(form.is_valid())

    def test_invalid_chart_type(self):
        form = RecipeSearchForm(data={**self.default_data, 'chart_type': ''})
        self.assertFalse(form.is_valid())

    def test_missing_chart_type(self):
        form = RecipeSearchForm(data={'recipe_title': 'Test Recipe'})
        self.assertFalse(form.is_valid())  # Chart type is required

class RecipeSearchViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setting up user and recipe data, similar to the RecipeModelTest
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.ingredient1 = Ingredient.objects.create(name="Butter")
        cls.ingredient2 = Ingredient.objects.create(name="Bread")
        cls.ingredient3 = Ingredient.objects.create(name="Cheese")
        cls.recipe1 = Recipe.objects.create(name='Butter Cheese Recipe', cook_time=10)
        cls.recipe2 = Recipe.objects.create(name='Cheese Salt Recipe', cook_time=15)
        cls.recipe1.ingredients.add(cls.ingredient1, cls.ingredient2)
        cls.recipe2.ingredients.add(cls.ingredient2, cls.ingredient3)

    def setUp(self):
        self.client.login(username='testuser', password='password')

    def test_recipe_search_with_title(self):
        # Simulating a search with a valid recipe title
        data = {'recipe_title': 'Cheese', 'chart_type': '#1'}
        response = self.client.post(reverse('recipes:search'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Butter Cheese Recipe')
        self.assertContains(response, 'Cheese Salt Recipe')

    def test_recipe_search_with_no_results(self):
        # Search for a recipe that doesn't exist
        data = {'recipe_title': 'Nonexistent', 'chart_type': '#1'}
        response = self.client.post(reverse('recipes:search'), data)
        
        self.assertEqual(response.status_code, 200)

    def test_recipe_search_all_recipes(self):
        # Search with 'all' to return all recipes
        data = {'recipe_title': 'all', 'chart_type': '#1'}
        response = self.client.post(reverse('recipes:search'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Butter Cheese Recipe')
        self.assertContains(response, 'Cheese Salt Recipe')

    def test_recipe_search_rendering_dataframe(self):
        # Check if DataFrame is correctly rendered in HTML
        data = {'recipe_title': 'Cheese', 'chart_type': '#1'}
        response = self.client.post(reverse('recipes:search'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<table')  # Check for the HTML table
        self.assertContains(response, 'Butter Cheese Recipe')  # Check that recipe data is in the table

    def test_recipe_search_chart(self):
        data = {'recipe_title': 'Cheese', 'chart_type': '#1'}  # Assuming chart_type #1 triggers chart generation
        response = self.client.post(reverse('recipes:search'), data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'chart')  # Check that the chart is rendered
    
  