import ast
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
from .get_recipe import *


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

        user_profile = Nutrition.objects.get(user=request.user)

        age = user_profile.age
        height = user_profile.height
        weight = user_profile.weight
        gender = user_profile.gender
        activity_level = user_profile.activity_level
        goal = user_profile.goal
        food_items = user_profile.food_items
        food_items = ast.literal_eval(food_items)

        food_items_dict = dict([(0, 'Crispy Fried Onions and Nori Topping Recipe'),
                                (1, 'Fried Noodles'),
                                (2, 'Fried Halloumi Cheese'),
                                (3, 'Fried Onion And Jalapeno Bison Burger Recipe'),
                                (4, 'Southern-fried chicken tacos'),
                                (5, 'Deep Fried Fish Bones'),
                                (6, 'Burnt-Scallion Fish'),
                                (7, 'Curry-Crusted Fish'),
                                (8, 'Fish in Coconut Sauce'),
                                (9, 'Homemade fish fingers'),
                                (10, 'Essentials: Rice'),
                                (11, 'Rice Cereal Bars'),
                                (12, 'Rice-Milk Rice Pudding'),
                                (13, 'Cooked Basmati Rice'),
                                (14, 'Rainbow rice'),
                                (15, 'Steak & Chips Salad'),
                                (16, 'Zuni-Inspired Grilled Chicken Salad'),
                                (17, 'Shrimp Salad'),
                                (18, 'Buffalo Chicken Salad')])
        user_recipes = []
        for item in food_items:
            recipe = {}
            temp_recipe = Fixed20Recipes.objects.get(name=food_items_dict[int(item)])
            recipe['yld'] = temp_recipe.yld
            recipe['calories'] = temp_recipe.calories / temp_recipe.yld
            recipe['fats'] = temp_recipe.fats / temp_recipe.yld
            recipe['sugar'] = temp_recipe.sugar / temp_recipe.yld
            recipe['protein'] = temp_recipe.protein / temp_recipe.yld
            recipe['carbs'] = temp_recipe.carbs / temp_recipe.yld
            user_recipes.append(recipe)

        print('\n ___________ USER RECIPES ___________')
        pprint(user_recipes)

        # for item in food_items:
        #     temp_recipe = Fixed20Recipes.objects.get(id=int(item)+1)
        #     print(temp_recipe)

        print(age, height, weight, gender, activity_level, goal, food_items)

        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        activity_factor = 1

        if activity_level.lower() == 'sedentary':
            activity_factor = 0.8
        elif activity_level.lower() == 'light':
            activity_factor = 1
        elif activity_level.lower() == 'moderate':
            activity_factor = 1.2
        elif activity_level.lower() == 'high':
            activity_factor = 1.4

        calorie_intake = round(bmr * activity_factor)

        if goal.lower() == 'lose':
            calorie_intake -= 300
        if goal.lower() == 'gain':
            calorie_intake += 300

        cal_per_dish = calorie_intake / 3
        carb_max = cal_per_dish / 8
        min_pro = weight * 2.2 * 0.8 / 4
        fat_max = cal_per_dish * 0.25 / 9
        sug_max = cal_per_dish / 40

        print(f'calorie per serve = {cal_per_dish}')

        searched_recipes = search_recipe(
            calories=cal_per_dish,
            health=health,
            cuisineType=cuisine_type,
            mealType=meal_type,
            carbMax=carb_max,
            fatMax=fat_max,
            sugarMax=sug_max,
            proMin=min_pro,
            diet=diet,
            q=recipe_query
        )
        print("\n______ Searched Recipes ____________")
        pprint(searched_recipes)

        sorted_recipes = find_nearest(user_recipes, searched_recipes)
        print("\n______ Sorted Recipes ____________")
        pprint(sorted_recipes)
        context = {
            'recipes': sorted_recipes
        }
        return render(request, 'recipe.html', {"recipes": sorted_recipes})

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
