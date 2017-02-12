from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='user_profile', on_delete=models.CASCADE)
    address = models.CharField(blank=True, null=True, max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile No. must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    mobile_number = models.CharField(validators=[phone_regex], blank=True, null=True,
                                     max_length=15)  # validators should be a list
    credit_card = models.IntegerField(blank=True, null=True)
    validation_code = models.CharField(max_length=100)
    enable = models.BooleanField()

    def __str__(self):
        return self.user.username


class UserRatingAvail(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_rating_avail', on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=100)


class UserRatingRender(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_rating_render', on_delete=models.CASCADE)
    rate = models.IntegerField()
    comment = models.CharField(max_length=100)


class Classification(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Job(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_jobs', on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, related_name='job_classification', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    date_start = models.CharField(max_length=8)
    date_end = models.CharField(max_length=8)
    fee = models.FloatField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    user = models.ForeignKey('auth.User', related_name='forums', on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name='application_job', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(default=False)
