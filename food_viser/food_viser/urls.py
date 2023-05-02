from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', mainPage.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    path('scan/', scan_label, name="scan"),
    path('nutrition_profile/', UserProfile.as_view(), name='nutrition_profile'),
    path('recipe-form/', RecipeFormView.as_view(), name="recipe-form"),
    path('show-recipe/', ShowRecipeView.as_view(), name='show-recipe'),
    path('nutrition/<slug:user_id>/', NutritionDetail.as_view(), name='nutrition'),
    # path('add-fixed-recipes/', add_fixed_recipes, name='add-fixed-recipes'),
]


