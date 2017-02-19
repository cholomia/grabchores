from django.contrib import admin
from .models import UserProfile, Classification, Job, JobApplication

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Classification)
admin.site.register(Job)
admin.site.register(JobApplication)
