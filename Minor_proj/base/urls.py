from django.urls import path
from .views import mainPage, UserLoginView, RegisterPage, User_Profile, NutritionDetail, MyView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', mainPage.as_view(), name='main'),
    path('view/', MyView.as_view(), name='view'),
    path('nutrition/<slug:user_id>/', NutritionDetail.as_view(), name='nutrition'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    path('nutrition_profile/', User_Profile.as_view(), name='nutrition_profile'),
    # path('scan/', scan_label, name="scan"),
]
