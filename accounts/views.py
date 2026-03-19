from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from datetime import timedelta
from .serializers import RegisterSerializer
from .models import User
from .emails import send_verification_email, send_welcome_email


class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Send verification email after registration
        try:
            send_verification_email(user)
        except Exception as e:
            print(f"Email send error: {e}")


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid verification link."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check token is not older than 24 hours
        expiry = user.verification_token_created + timedelta(hours=24)
        if timezone.now() > expiry:
            return Response(
                {"error": "Verification link has expired. Please register again."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user.email_verified:
            return Response(
                {"message": "Email already verified. Please log in."},
                status=status.HTTP_200_OK
            )

        # Activate the account
        user.is_active      = True
        user.email_verified = True
        user.save()

        # Send welcome email
        try:
            send_welcome_email(user)
        except Exception as e:
            print(f"Welcome email error: {e}")

        return Response(
            {"message": "Email verified successfully. You can now log in."},
            status=status.HTTP_200_OK
        )


class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Don't reveal if email exists
            return Response(
                {"message": "If that email exists, a verification link has been sent."},
                status=status.HTTP_200_OK
            )

        if user.email_verified:
            return Response(
                {"error": "This email is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Reset token and resend
        import uuid
        user.verification_token         = uuid.uuid4()
        user.verification_token_created = timezone.now()
        user.save()

        try:
            send_verification_email(user)
        except Exception as e:
            print(f"Resend email error: {e}")

        return Response(
            {"message": "Verification email resent."},
            status=status.HTTP_200_OK
        )