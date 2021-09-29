from django.contrib import admin
from .models import User,FailedLogins

# Register your models here.

admin.site.register(User)
admin.site.register(FailedLogins)

