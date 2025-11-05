from cloudinary.forms import CloudinaryFileField, CloudinaryInput
from django import forms
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio',)
    
    image = CloudinaryFileField(
        options={"folder": "foodfeed/", "crop": "limit", "width": 600, "height": 600,})
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False
        self.fields['image'].label = "Profile picture"
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['username'].help_text = "150 characters or fewer. Letters, digits and @/./+/-/_ only."