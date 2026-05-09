# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    USER_TYPE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (VENDOR, 'Vendor'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CUSTOMER)

    def is_vendor(self):
        return self.user_type == self.VENDOR

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=255)
    store_description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)   # admin approval

    def __str__(self):
        return self.store_name