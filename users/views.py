from django.contrib.auth import views
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from .forms import LoginForm, ProfileEditForm
from .forms import SignUpForm
from .models import User


class SignUp(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        form.save()
        return valid


class LoginView(views.LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class LogoutView(views.LogoutView):
    success_url = '/'


class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/profile_edit.html'

    def get_success_url(self):
        return reverse('posts:main')

