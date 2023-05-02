import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormView, CreateView
# use for profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import Profile
from .nutrition import get_nutrition
from django.core.files.storage import default_storage
import cv2

from .models import Fixed20Recipes, Nutrition
from .get_recipe import search_recipe

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
    success_url = reverse_lazy('nutrition_profile')

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


class UserProfile(LoginRequiredMixin, CreateView):
    model = Nutrition
    success_url = reverse_lazy('main')
    template_name = 'nutrition_profile_form.html'
    form_class = Profile

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserProfile, self).form_valid(form)


class NutritionDetail(DetailView):
    model = Nutrition
    context_object_name = 'nutrition'
    template_name = 'nutrition_detail.html'
    slug_url_kwarg = "user_id"
    slug_field = "user_id"


class RecipeFormView(View):
    def get(self, request):
        return render(request, 'recipe_form.html')


class ShowRecipeView(View):

    def post(self, request):
        recipe_query = request.POST.get('recipe_query', None)
        health = request.POST.get('health', None)
        cuisine_type = request.POST.get('cuisine_type', None)
        meal_type = request.POST.get('meal_type', None)
        diet = request.POST.get('diet', None)

        # Do something with the data, such as querying a database
        # and returning the results as a JSON response
        data = {
            'recipe_query': recipe_query,
            'health': health,
            'cuisine_type': cuisine_type,
            'meal_type': meal_type,
            'diet': diet
        }
        print(data)
        # recipes = search_recipe()
        return render(request, 'show_recipe.html')

# def add_fixed_recipes(request):
#     with open(r"C:\Users\Gitesh\OneDrive\Documents\GitHub\nutrition_analyser\food_viser\food_viser\recipes.json", 'r') as f:
#         data = json.load(f)
#
#     for recipe, det in data['recipes'].items():
#         name = recipe
#         image = det['image']
#         yld = det['yield']
#         calories = det['calories']
#         fats = det['totalNutrients']['FAT']['quantity']
#         carbs = det['totalNutrients']['CHOCDF']['quantity']
#         sugar = det['totalNutrients']['SUGAR']['quantity']
#         protein = det['totalNutrients']['PROCNT']['quantity']
#
#         print(name, yld, calories, fats, carbs, sugar, protein)
#         recipe = Fixed20Recipes(name=name, image=image, yld=yld, calories=calories, fats=fats, carbs=carbs, sugar=sugar,
#                                 protein=protein)
#         recipe.save()
#     return render(request, 'success.html')
