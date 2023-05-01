from django.db import models
from django.contrib.auth.models import User


class NutritionProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    weight = models.IntegerField()
    age = models.IntegerField()
    height = models.IntegerField()
    gender = models.CharField(max_length=6, choices=[('male', 'Male'), ('female', 'Female')])
    activity_level = models.CharField(max_length=10,
                                      choices=[('sedentary', 'Sedentary'), ('light', 'Light'), ('moderate', 'Moderate'),
                                               ('high', 'High')])
    goal = models.CharField(max_length=8, choices=[('lose', 'Lose'), ('maintain', 'Maintain'), ('gain', 'Gain')])
