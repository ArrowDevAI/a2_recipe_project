from django.test import TestCase

from django.test import TestCase
from .models import Ingredient

class IngredientModelTest(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Tomato")

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Tomato")

    def test_ingredient_str_method(self):
        self.assertEqual(str(self.ingredient), "Tomato")
