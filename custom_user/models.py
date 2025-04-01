from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.db import models
from django.utils.timezone import now
from datetime import timedelta
import random

class User(BaseUser):
    objects = BaseUserManager()
    
    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expiry = models.DateTimeField(blank=True, null=True)  # ✅ Expiry field

    def generate_verification_code(self):
        """Generates a 6-digit code and sets an expiration time (5 mins)."""
        self.verification_code = f"{random.randint(100000, 999999)}"
        self.verification_code_expiry = now() + timedelta(minutes=5)

    def is_verification_code_valid(self):
        """Checks if the verification code is still valid."""
        return self.verification_code and self.verification_code_expiry and now() < self.verification_code_expiry

    def save(self, *args, **kwargs):
        """Generates a new code if missing and saves the user."""
        if not self.verification_code:
            self.generate_verification_code()
        super().save(*args, **kwargs)
