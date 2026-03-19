from django.urls import path
from .views import GoogleLoginView, RegisterView,VerifyEmailView, ResendVerificationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(),  name='verify_email'),
    path('resend-verification/',  ResendVerificationView.as_view(),name='resend_verification'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
]

