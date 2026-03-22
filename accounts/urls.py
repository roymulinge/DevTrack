from django.urls import path
from .views import (
    RegisterView, VerifyEmailView, ResendVerificationView,
    GoogleLoginView, ChangePasswordView, ProfileView, DeleteAccountView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/',                  RegisterView.as_view(),            name='register'),
    path('login/',                     TokenObtainPairView.as_view(),     name='token_obtain_pair'),
    path('token/refresh/',             TokenRefreshView.as_view(),        name='token_refresh'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(),        name='verify_email'),
    path('resend-verification/',       ResendVerificationView.as_view(),  name='resend_verification'),
    path('google/',                    GoogleLoginView.as_view(),         name='google_login'),
    path('change-password/',           ChangePasswordView.as_view(),      name='change_password'),
    path('me/',                        ProfileView.as_view(),             name='profile'),
    path('delete/',                    DeleteAccountView.as_view(),       name='delete_account'),
]

