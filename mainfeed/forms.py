from cloudinary.forms import CloudinaryFileField
from .models import Post, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')
    
    image = CloudinaryFileField(
        options={"folder": "foodfeed/", "crop": "limit", "width": 600, "height": 600,}
     )
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)