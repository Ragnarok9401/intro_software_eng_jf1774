from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    ##still figuring this out
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username   ##youtube told me to do this