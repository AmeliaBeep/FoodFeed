from cloudinary.forms import CloudinaryFileField
from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'image')
    
    image = CloudinaryFileField(
        options={"folder": "foodfeed/", "crop": "limit", "width": 600, "height": 600,}
        )
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = "Image to share"
        self.fields['text'].label = "Post text"
    
class PostTextForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(PostTextForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Post text"
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].label = "Comment text"