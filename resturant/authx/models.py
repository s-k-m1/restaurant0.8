from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

#============================ Custom User =================
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(region="NP", unique=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"        #email baata login garna
    REQUIRED_FIELDS = ["username", "full_name", "phone_number"]     #superuser banauda

    class Meta:
        db_table = 'custom_user'

class Otp(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_otp")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    expired_at = models.DateTimeField()

    class Meta:
        db_table = 'otp'
     
class Profile(models.Model):
        user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='user_profile')
        profile_pic = models.ImageField(upload_to = "profile/", null =True, blank= True)
        date_of_birth = models.DateField(null = True, blank = True )
        gender = models.CharField(max_length=6, null =True, blank = True)
        created_at = models.DateField(default= timezone.now)
        updated_at = models.DateField(null= True, blank = True)
        
        class Meta:
            db_table = 'profile'