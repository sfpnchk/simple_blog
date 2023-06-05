from django.urls import path

from .views import SignUp, LoginView, LogoutView, ProfileUpdateView

app_name = "user"

urlpatterns = [
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>", ProfileUpdateView.as_view(), name="profile"),
]
