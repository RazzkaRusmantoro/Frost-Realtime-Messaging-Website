from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField



# Create your models here.
# class Note(models.Model):
    # title = models.CharField(max_length = 100)
    # content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True) 


class CustomUser(AbstractUser):
    biography = models.TextField(blank=True, null=True)
    profile_image = CloudinaryField('image', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_perms',
        blank=True
    )

    def __str__(self):
        return self.username
