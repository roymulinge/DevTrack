from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def send_verification_email(user):
    verify_url = (
        f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}"
    )

    subject = "Verify Your DevTrack Account"