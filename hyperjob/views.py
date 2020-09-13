from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django import forms
from django.db import models
from django.contrib.auth.models import User
from resume.models import Resume
from vacancy.models import Vacancy
import sys
sys.path.append("..")


class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "Main.html")


class MySignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'login.html'


class CustomForm(forms.Form):
    description = forms.CharField(max_length=1024)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        custom_form = CustomForm()
        return render(request, 'home.html', context={'custom_form': custom_form})


class NewView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied
        if not request.user.is_staff and request.path == '/vacancy/new':
            raise PermissionDenied
        if request.user.is_staff and request.path == '/resume/new':
            raise PermissionDenied
        my_form = CustomForm(data=request.POST)
        if my_form.is_valid():
            my_description = my_form.cleaned_data['description']
            if request.user.is_staff:
                Vacancy.objects.create(description=my_description, author=request.user)
                return redirect('/home')
            else:
                Resume.objects.create(description=my_description, author=request.user)
                return redirect('/home')
