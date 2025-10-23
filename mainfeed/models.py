from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_posts")
    photo = CloudinaryField('image', default='placeholder')
    text = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    #updated_on = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ["-created_on"]
    
    def __str__(self):
        return f"Post written by {self.author}"