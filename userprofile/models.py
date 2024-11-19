from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class Passenger(AbstractUser):
    IDENTITY_DOC_CHOICES = [
        ('National Identity Card', 'National Identity Card'),
        ('Passport', 'Passport'),
        ('Resident Card', 'Resident Card'),
    ]
    
    phone = models.CharField(max_length=15, blank=True, null=True)
    identity_document = models.CharField(max_length=30, choices=IDENTITY_DOC_CHOICES)
    dob = models.DateField(default=timezone.now)
    part_no = models.CharField(max_length=30, null=False, blank=False)
    profile_pic = models.ImageField(upload_to='profile', null=True, blank=True)
    
    # Use related_name to avoid conflicts with the default User model
    groups = models.ManyToManyField(Group, related_name='passenger_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='passenger_user_permissions')

    def __str__(self):
        return self.username