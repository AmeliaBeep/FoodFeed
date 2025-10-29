from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here


class UserProfile(models.Model):
    """
    A UserProfile based on User that adds a bio and profile picture.

    A one-to-one relationship is created between the fields in the User model.

    AUTH_USER_MODEL defaults to 'auth.User' if not set manually.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField()
    image = CloudinaryField('image', default='static/images/no-user-image.jpg')

    def __str__(self):
        return f"{self.user}" 
