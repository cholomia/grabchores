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
