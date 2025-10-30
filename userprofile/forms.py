from cloudinary.forms import CloudinaryFileField
from .models import UserProfile
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('image', 'bio')
    
    image = CloudinaryFileField(
        options={"folder": "foodfeed/", "crop": "limit", "width": 600, "height": 600,}
        )