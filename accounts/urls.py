from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import SignupView, CustomLoginView, current_physician, ResetPasswordView


urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", current_physician, name="current_physician"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
]
