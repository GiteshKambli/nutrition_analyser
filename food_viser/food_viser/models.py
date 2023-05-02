from django.db import models
from django.contrib.auth.models import User


class Nutrition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=6)
    activity_level = models.CharField(max_length=10)
    goal = models.CharField(max_length=8)
    food_items = models.CharField(max_length=100)


class Fixed20Recipes(models.Model):
    name = models.CharField(max_length=1000)
    image = models.CharField(max_length=5000)
    yld = models.FloatField()
    calories = models.FloatField()
    fats = models.FloatField()
    carbs = models.FloatField()
    sugar = models.FloatField()
    protein = models.FloatField()
