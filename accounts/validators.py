import logging
import dns.resolver
from rest_framework import serializers
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

logger = logging.getLogger(__name__)

BLOCKED_DOMAINS = {
    'mailinator.com', 'tempmail.com', 'guerrillamail.com',
    'throwam.com', 'sharklasers.com', 'yopmail.com',
    'trashmail.com', 'fakeinbox.com', 'dispostable.com',
    'maildrop.cc', 'temp-mail.org', 'getnada.com',
    'spam4.me', 'grr.la', 'getairmail.com',
}


def validate_email(value):
    email = value.lower().strip()

    try:
        django_validate_email(email)
    except DjangoValidationError:
        raise serializers.ValidationError("Enter a valid email address.")
    
    domain = email.split('@')[-1]

    try:
        dns.resolver.resolve(domain, 'MX')
    except dns.resolver.NXDOMAIN:
        raise serializers.ValidationError(
            f"'{domain}' does not exist. Check your email for typos"
        )
    except dns.resolver.NoAnswer:
        raise serializers.ValidationError(
            f"'{domain}' cannot receive email. Use an address from a mail provider."
        )
    except (dns.resolver.TimeOut, Exception):
        logger.waring(f"DNS lookup failed for domain: {domain}")

    if domain in BLOCKED_DOMAINS:
        raise serializers.ValidationError(
            "Please use a real email address from a reputable provider."
        )
    
    return email 
