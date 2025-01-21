from django.db import models
from ingredients.models import Ingredient
from django.core.validators import MinValueValidator
from django.urls import reverse


class Recipe(models.Model):
    name = models.CharField(max_length = 75)
    difficulty = models.CharField(max_length = 12, editable = False)
    cook_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Time in minutes')
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    pic = models.ImageField(upload_to='recipes/', default='recipes/no_picture.jpg')

    def calc_difficulty(self):

        cook_time = self.cook_time
        num_ingredients = self.ingredients.count()

        if num_ingredients < 4 and cook_time < 10:
            self.difficulty = "Easy"
        elif cook_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif cook_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else: 
            self.difficulty = "Hard"

        return self.difficulty

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calc_difficulty()
        super().save(update_fields=['difficulty'])


    def __str__(self):
        num_ingredients = self.ingredients.count()
        return (
            f"Name: {self.name} | Cook Time: {self.cook_time} mins | "
            f"Difficulty: {self.difficulty} | Ingredients: {num_ingredients}"
        )
    
        
    def get_absolute_url(self):
       return reverse('recipes:detail', kwargs={'pk': self.pk})
