from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
import uuid
from .serializers import RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from .models import User
from .emails import send_verification_email, send_welcome_email
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from projects.models import Project, Assignment
from skills.models import Skill
from ideas.models import Idea
from rest_framework.throttling import UserRateThrottle

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.core.mail import send_mail
class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        user.is_active      = True
        user.email_verified = True
        user.save()


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

        user.is_active      = True
        user.email_verified = True
        user.save()

        send_welcome_email(user)  # no try/except — show real errors

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
            return Response(
                {"message": "If that email exists, a verification link has been sent."},
                status=status.HTTP_200_OK
            )

        if user.email_verified:
            return Response(
                {"error": "This email is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.verification_token         = uuid.uuid4()
        user.verification_token_created = timezone.now()
        user.save()

        send_verification_email(user)  # no try/except — show real errors

        return Response(
            {"message": "Verification email resent."},
            status=status.HTTP_200_OK
        )
    
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("credential")
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
        except ValueError:
            return Response({"error": "Invalid Google token."}, status=status.HTTP_400_BAD_REQUEST)

        email     = idinfo.get("email")
        full_name = idinfo.get("name", "")

        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "full_name": full_name,
                "email_verified": True,
                "is_active": True,
            }
        )

        # If user exists but not verified, verify them
        if not user.email_verified:
            user.email_verified = True
            user.is_active = True
            user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "access":  str(refresh.access_token),
            "refresh": str(refresh),
        })
    
class ChangePasswordThrottle(UserRateThrottle):
    scope = 'change_password'
    
class ChangePasswordView(APIView):
    permission_classes =[IsAuthenticated]
    throttle_classes = [ChangePasswordThrottle]
    def post(self, request):
   
        serializer = ChangePasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user

        old_password =serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(old_password):
            return Response(
                {"error": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.check_password(new_password):
            return Response(
                {"error":"New password must be different from your current password."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()

        tokens =OutstandingToken.objects.filter(user=user)

        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response(
            {"message": "password changed successfully.Please log in again"},
            status=status.HTTP_200_OK
        )
     
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id":             user.id,
            "email":          user.email,
            "full_name":      user.full_name,
            "email_verified": user.email_verified,
            "member_since":   user.verification_token_created,
            "stats": {
                "projects":    Project.objects.filter(owner=user).count(),
                "skills":      Skill.objects.filter(owner=user).count(),
                "assignments": Assignment.objects.filter(owner=user).count(),
                "ideas":       Idea.objects.filter(owner=user).count(),
            }
        })

    def patch(self, request):
        user      = request.user
        full_name = request.data.get("full_name", "").strip()
        if not full_name:
            return Response(
                {"error": "Full name cannot be empty."},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.full_name = full_name
        user.save()
        return Response({"message": "Profile updated.", "full_name": user.full_name})


class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            reset_link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"

            send_mail(
                subject="Reset your password",
                message=f"Use this link:\n{reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

        return Response(
            {"message": "If an account with this email exists, a password reset link has been sent."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        new_password = serializer.validated_data['password']

        if user.check_password(new_password):
            return Response(
                {"error": "New password must be different from the old password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        # 🔐 Invalidate all JWT sessions (same pattern you already use)
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response(
            {"message": "Password reset successful. Please log in."},
            status=status.HTTP_200_OK
        )