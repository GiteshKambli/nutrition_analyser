from django import forms
from .models import Nutrition
import json

gender_choices=[('male', 'Male'), ('female', 'Female')]
goal_choices=[('lose', 'Lose'), ('maintain', 'Maintain'), ('gain', 'Gain')]
activity_choices=[('sedentary', 'Sedentary'), ('light', 'Light'), ('moderate', 'Moderate'),('high', 'High')]

with open('recipes.json', 'r') as f:
    data = json.load(f)

food_items = []
count = 0

for recipe_name in data['recipes']:
    food_items.append(recipe_name)
    count += 1
    if count >= 20:
        break

print(food_items)

choices = {}
for i in range(len(food_items)):
    choices[i] = food_items[i]

print(choices)
class Profile(forms.ModelForm):
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect())
    goal = forms.ChoiceField(choices=goal_choices, widget=forms.RadioSelect())
    activity_level = forms.ChoiceField(choices=activity_choices, widget=forms.RadioSelect())
    
    food_items = forms.MultipleChoiceField(label='Preferred Food Items', choices=choices, widget=forms.CheckboxSelectMultiple())
    
    class Meta:
        model = Nutrition
        fields = ['weight', 'age', 'height', 'gender', 
                  'activity_level', 'goal', 'food_items']
        
        widgets = {
            'weight':forms.NumberInput(attrs={'class': 'form-control'}),
            'age':forms.NumberInput(attrs={'class': 'form-control'}),
            'height':forms.NumberInput(attrs={'class': 'form-control'}),
        }