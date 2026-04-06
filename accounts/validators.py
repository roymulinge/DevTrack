import logging
import dns.resolver
from rest_framework import serializers
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

logger = logging.getLogger(__name__)