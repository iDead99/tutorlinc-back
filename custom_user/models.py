from django.db import models
import uuid
from datetime import timedelta
from django.utils.timezone import now
from django_use_email_as_username.models import BaseUser, BaseUserManager

class User(BaseUser):
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)  # Track token creation time
    is_active = models.BooleanField(default=False)

    objects = BaseUserManager()

    def generate_verification_token(self):
        self.verification_token = str(uuid.uuid4())
        self.token_created_at = now()
        self.save()
	
    def is_token_expired(self):
        if self.token_created_at:
            expiration_time = self.token_created_at + timedelta(hours=24)
            return now() > expiration_time
        return True