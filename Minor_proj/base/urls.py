from django.urls import path
from .views import mainPage, UserLoginView, RegisterPage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', mainPage.as_view(), name='main'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='main'), name='logout'),
    # path('scan/', scan_label, name="scan"),
]
