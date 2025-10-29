from django.db import models
from userprofile.models import UserProfile
from cloudinary.models import CloudinaryField

# Create your models here

class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="users_posts")
    image = CloudinaryField('image', default='static/images/default.jpg')
    text = models.TextField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]
    
    def __str__(self):
        return f"Post written by {self.author} starting '{self.text[:30]}'"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}" 