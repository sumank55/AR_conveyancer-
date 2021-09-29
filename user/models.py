from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager


# Create your models here.
class UserPermission(models.Model):
    is_admin = models.BooleanField(default=False)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, username=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=email
        )

        user_permission = UserPermission(
            is_admin=True
        )
        user_permission.save()

        user.permissions = user_permission
        user.set_password(password)

        user.is_admin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(unique=False, max_length=100, null=True, blank=True)
    first_name= models.CharField(max_length=50, null=True, blank=True)
    last_name= models.CharField(max_length=50, null=True, blank=True)
    business_name= models.CharField(max_length=50, null=True, blank=True)
    contact_number= models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    is_locked = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def get_user_email(self):
        return self.email


class FailedLogins(models.Model):
    failed_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    
    def __str__(self):
        return str(self.failed_count)