from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic.detail import DetailView
#use for profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import Profile
from .models import Nutrition

# Create your views here.
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
    


class User_Profile(LoginRequiredMixin, CreateView):
    model = Nutrition
    success_url = reverse_lazy('main') 
    template_name = 'nutrition_profile_form.html'
    form_class = Profile

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(User_Profile, self).form_valid(form)
    

class NutritionDetail(DetailView):
    model = Nutrition
    context_object_name = 'nutrition'
    template_name = 'nutrition_detail.html'
    slug_url_kwarg = "user_id"
    slug_field = "user_id"