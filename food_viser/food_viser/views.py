import json

from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
# use for profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .nutrition import get_nutrition
from django.core.files.storage import default_storage
import cv2

from .models import NutritionProfile, Fixed20Recipes


class mainPage(View):
    template_name = 'main.html'

    def get(self, request):
        return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["main"] = context['main'].filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(mainPage, self).form_valid(form)


class UserLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('main')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('main')
        return super(RegisterPage, self).get(*args, **kwargs)


def scan_label(request):
    if request.method == 'POST':
        f = request.FILES['sentFile']  # here you get the files needed
        response = {}
        file_name = "pic.jpg"
        file_name_2 = default_storage.save(file_name, f)
        file_url = r'../food_viser/' + default_storage.url(file_name_2)
        print(file_url)
        img = cv2.imread(file_url)
        nutrition = get_nutrition(img, ocr='easyocr')

        return render(request, 'scan.html', {'nutrition': nutrition[0]})

    return render(request, 'scan.html')


class NutritionProfileView(View):
    def get(self, request):
        # Render the template for the form
        return render(request, 'nutrition_profile_form.html')

    def post(self, request):
        # Get the data from the form
        weight = request.POST.get('weight')
        age = request.POST.get('age')
        height = request.POST.get('height')
        gender = request.POST.get('gender')
        activity_level = request.POST.get('activity_level')
        goal = request.POST.get('goal')

        # Create a new NutritionProfile object with the data
        nutrition_profile = NutritionProfile(
            user=request.user,  # assuming the user is authenticated
            weight=weight,
            age=age,
            height=height,
            gender=gender,
            activity_level=activity_level,
            goal=goal
        )

        # Save the NutritionProfile object to the database
        nutrition_profile.save()

        # Render a success message
        return render(request, 'main.html')

def recipe_search(request):
    return render(request, 'recipe.html')


def add_fixed_recipes(request):
    with open(r"C:\Users\Gitesh\OneDrive\Documents\GitHub\nutrition_analyser\food_viser\food_viser\recipes.json", 'r') as f:
        data = json.load(f)

    for recipe, det in data['recipes'].items():
        name = recipe
        image = det['image']
        yld = det['yield']
        calories = det['calories']
        fats = det['totalNutrients']['FAT']['quantity']
        carbs = det['totalNutrients']['CHOCDF']['quantity']
        sugar = det['totalNutrients']['SUGAR']['quantity']
        protein = det['totalNutrients']['PROCNT']['quantity']

        print(name, yld, calories, fats, carbs, sugar, protein)
        recipe = Fixed20Recipes(name=name, image=image, yld=yld, calories=calories, fats=fats, carbs=carbs, sugar=sugar,
                                protein=protein)
        recipe.save()
    return render(request, 'success.html')
