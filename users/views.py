from django.contrib.auth import views
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView

from .forms import LoginForm
from .forms import SignUpForm
from .models import User


class SignUp(CreateView):
    model = User
    template_name = 'users/signup.html'
    form_class = SignUpForm
    success_url = '/'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        user = form.save()
        scheme = self.request.scheme
        domain = get_current_site(self.request).domain
        return valid


class LoginView(views.LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm


class LogoutView(views.LogoutView):
    success_url = '/'

