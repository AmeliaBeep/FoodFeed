from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models

# Create your models here


class UserProfile(models.Model):
    """
    A UserProfile based on User that adds a bio and profile picture.

    A one-to-one relationship is created between this model and the User model.

    AUTH_USER_MODEL defaults to 'auth.User' if not set manually.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile")
    bio = models.TextField(max_length=800, blank=True)
    image = CloudinaryField('image', default='no-profile-image')

    def __str__(self):
        return f"{self.user}" 
