from django import forms

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

class RecipeSearchForm(forms.Form):
    recipe_title = forms.CharField(max_length=120)
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    
