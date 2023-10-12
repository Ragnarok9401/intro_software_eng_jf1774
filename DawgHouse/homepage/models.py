from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.db.models.signals import post_save

User = get_user_model()

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)                           ##still figuring this out
    bio = models.TextField(blank=True)
    follows = models.ManyToManyField(
        "self", 
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username   
    
class Bark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    num_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user
    
def create_profile(sender, instance, created, ** kwargs):       #creates profile when user is created
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Relationship(models.Model):
    from_user = models.ForeignKey(User,related_name='following', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='followers', on_delete=models.CASCADE)

    def __str__(self):
        return '{} follows {}'.format(self.from_user, self.to_user)
