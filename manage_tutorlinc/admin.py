from django.contrib import admin
from . models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display=['user', 'phone', 'highest_qualification', 'availability_status', 'profile_picture']
    list_per_page=10
    list_select_related = ['user']
    list_filter=['user']
    ordering=['availability_status', 'user']
    search_fields=['phone']
