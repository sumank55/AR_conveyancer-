from django.db import models
from user.models import User
from tradie.models import Tradie


# Create your models here.

# iterable
STATUS_CHOICES =(
    ("Building", "Building"),
    ("Complate", "Complate"),
    ("Planned", "Planned"),
)

class Project(models.Model):
    project_id = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_details = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    plans = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=50, default="Planned", null=True, blank=True)
    file = models.FileField(upload_to='project-images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_id


class ProjectTradie(models.Model):
    project_id = models.CharField(max_length=50, null=True, blank=True)
    tradie_id = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return self.project_id
