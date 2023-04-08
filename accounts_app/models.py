from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    avatar=models.ImageField(upload_to="avatar/",null=True,blank=True,default="avatar/images.png")
    email = models.EmailField(unique=True,null=True,blank=True)
    phone_number = models.CharField(max_length=11, unique=True)
    is_admin=models.BooleanField(default=False)
    full_name = models.CharField(max_length=64,null=True,blank=True)
    status = models.JSONField(default=dict,null=True,blank=True)
    user_type = models.CharField(max_length=24,null=True,blank=True)
    limit=models.IntegerField(default=10)
    manager=models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_manager(self):
        return self.manager
        
class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    otp = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone_number} - {self.otp}'
