from django.db import models
from user.models import User


# Create your models here.


class Tradie(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    contact_details = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    active_plans = models.CharField(max_length=20, null=True, blank=True)
    status = models.BooleanField(default=False, null=True, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name