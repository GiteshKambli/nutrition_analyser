from django.db import models
from django.forms import fields
from .models import UploadImage
from django import forms


class UserImageForm(forms.ModelForm):
    class Meta:
        # To specify the model to be used to create form
        model = UploadImage
        # It includes all the fields of model
        fields = '__all__'
