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