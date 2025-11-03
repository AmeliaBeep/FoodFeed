from django.test import TestCase

from userprofile.forms import UserForm, UserProfileForm
import cloudinary.api
import requests
from cloudinary.uploader import destroy
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError


class TestProfileUser(TestCase):
    """
    Test cases to validate the UserProfile model.

    These test cases are those not covered by those in test_forms.py as 
    UserProfileForm does not handle the user field.
    """

    # TODO: Mock Cloudinary response in creating test_image
    #       Prevent PostForm to_python subroutines from uploading test_image     
    def test_model_is_valid(self):
        """ 
        Tests that UserProfile accepts valid fields.
        """
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}
        test_user_profile_form = UserProfileForm({'bio': 'Test bio text'}, image)

        test_user_form = UserForm(data={'username': 'test_username'})
        user = test_user_form.save()

        test_user_profile = test_user_profile_form.save(commit=False)
        test_user_profile.user = user
        
        test_user_profile.save()
        test_user_profile.full_clean()

        uploaded_asset_id = test_user_profile_form.cleaned_data['image'].public_id
        cloudinary.uploader.destroy(uploaded_asset_id)

    def test_model_has_no_user(self):
        """ 
        Tests that UserProfile rejects missing user.
        """

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}

        test_user_profile_form = UserProfileForm({'bio': 'Test bio text'}, image)

        with self.assertRaises(IntegrityError, msg="User Profile able to be saved to database, but no user provided"):
            test_user_profile_form.save()

        uploaded_asset_id = test_user_profile_form.cleaned_data['image'].public_id
        cloudinary.uploader.destroy(uploaded_asset_id)

        

    