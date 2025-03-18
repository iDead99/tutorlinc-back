import os
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from .validators import validate_file_size
import cloudinary.uploader

class Teacher(models.Model):
    active = 'Active'
    inactive = 'Inactive'
    AVAILABILITY_CHOICES = [
        (active, active),
        (inactive, inactive)
    ]

    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    highest_qualification = models.CharField(max_length=50)
    availability_status = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default=active)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        validators=[validate_file_size],                                
        blank=True
    )
           
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    # def save(self, *args, **kwargs):
    #     """Deletes the old profile picture from storage when a new one is uploaded."""
    #     if self.pk:  # Ensure the instance already exists
    #         old_instance = Teacher.objects.filter(pk=self.pk).first()
    #         if old_instance and old_instance.profile_picture:  # Ensure there is an existing profile picture
    #             if self.profile_picture and self.profile_picture != old_instance.profile_picture:
    #                 old_image_path = old_instance.profile_picture.path
    #                 if os.path.exists(old_image_path):
    #                     os.remove(old_image_path)
    #     super().save(*args, **kwargs)

def save(self, *args, **kwargs):
    """Deletes the old profile picture from Cloudinary when a new one is uploaded."""
    if self.pk:  # Ensure the instance already exists
        old_instance = Teacher.objects.filter(pk=self.pk).first()
        if old_instance and old_instance.profile_picture:  # Ensure there is an existing profile picture
            if self.profile_picture and self.profile_picture != old_instance.profile_picture:
                # Extract the Cloudinary public ID from the URL
                public_id = old_instance.profile_picture.public_id
                if public_id:
                    cloudinary.uploader.destroy(public_id)  # Deletes the old image from Cloudinary

    super().save(*args, **kwargs)



class Subject(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    day_to_teach = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_index=True)

class Address(models.Model):
    region = models.CharField(max_length=255, db_index=True)
    town = models.CharField(max_length=255, db_index=True)
    street = models.CharField(max_length=255, db_index=True)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True, db_index=True)

class Verification(models.Model):
    ALLOWED_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf']

    id_card = models.FileField(
        upload_to='verification_certificates/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_FILE_EXTENSIONS), validate_file_size]
    )
    certificate = models.FileField(
        upload_to='verification_certificates/',
        validators=[FileExtensionValidator(allowed_extensions=ALLOWED_FILE_EXTENSIONS), validate_file_size]
    )
    id_verification = models.BooleanField(default=False)
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, primary_key=True, db_index=True)

class Inquiry(models.Model):
    student_name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, db_index=True)  # Useful if filtering inquiries by phone
    message = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_index=True)

class Comment(models.Model):
    comment = models.TextField()
    commenter = models.CharField(max_length=255, null=True, blank=True)
    rate = models.IntegerField(default=0, null=True, blank=True)
