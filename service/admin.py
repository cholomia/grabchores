from django.contrib import admin
from .models import UserProfile, Classification, Job

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Classification)
admin.site.register(Job)
