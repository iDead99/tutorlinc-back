from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Teacher

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_teacher_for_new_user(sender, **kwargs):
    if kwargs['created']:
        Teacher.objects.create(user=kwargs['instance'])