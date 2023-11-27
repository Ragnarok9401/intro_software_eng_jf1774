"""
Contains Models For DawgHouse
"""

import uuid
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.db import models

# Create your models here.

class DawgHouseUserManager(BaseUserManager):
    """Commits new user to database"""
    def create_user(
        self, username, password=None, first_name=None, last_name=None, **extra_fields
    ):
        """Adds regular user to databse"""
        if not username:
            raise ValueError("You must enter a DawgTag")
        if not first_name:
            raise ValueError("You must enter your first name")
        if not last_name:
            raise ValueError("You must enter your last name")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, password=None, first_name=None, last_name=None, **extra_fields
    ):
        """Adds admin to database"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(
            username, password, first_name, last_name, **extra_fields
        )


class DawgHouseUser(AbstractBaseUser, PermissionsMixin):
    """Defines user model for database"""
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, max_length=200)
    friends = models.ManyToManyField("self", blank=True)
    is_staff = models.BooleanField(default=False)
    profile_picture = models.CharField(max_length=100, default="images/profilePicture.jpg")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = DawgHouseUserManager()


class SniffRequest(models.Model):
    """Defines sniff request model for database"""
    from_user = models.ForeignKey(
        DawgHouseUser, related_name="form_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        DawgHouseUser, related_name="to_user", on_delete=models.CASCADE
    )


class Bark(models.Model):
    """Defines bark model for database"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    num_likes = models.IntegerField(default=0)
    num_yips = models.IntegerField(default=0)
    num_howls = models.IntegerField(default=0)
    treated_by = models.ManyToManyField(
        DawgHouseUser, related_name="treats_given", blank=True
    )

    is_repost = models.BooleanField(default=False)
    original_bark=models.ForeignKey('self',null=True,blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Returns user posting bark"""
        return str(self.user)

class Comment(models.Model):
    """Defines comment model for database"""
    bark = models.ForeignKey(Bark, related_name="comments", on_delete=models.CASCADE)
    name = models.ForeignKey(DawgHouseUser, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
    #   return '%s - %s' % (self.bark.content, self.name)
    