import cloudinary.api
import requests
from cloudinary.uploader import destroy
from django.core.files.base import ContentFile
from django.test import TestCase

from .forms import UserForm, UserProfileForm


class TestProfileUserForm(TestCase):
    """Test cases to validate the UserProfileForm model form."""

    def test_form_is_valid(self):
        """Tests that PostForm accepts valid bio and image fields."""

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')

        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}

        form = UserProfileForm({'bio': 'Test bio text'}, image)

        self.assertTrue(form.is_valid(),
                        msg='Form is not valid, but it should be')

        uploaded_asset_id = form.cleaned_data['image'].public_id
        cloudinary.uploader.destroy(uploaded_asset_id)

    def test_form_is_missing_bio(self):
        """Tests that UserProfileForm accepts submissions with empty bio
        field."""

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')

        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}

        form = UserProfileForm(data={'bio': ''}, files=image)

        self.assertTrue(
            form.is_valid(), msg='Form is invalid, but empty bio should be accepted')
        uploaded_asset_id = form.cleaned_data['image'].public_id
        cloudinary.uploader.destroy(uploaded_asset_id)

    def test_form_is_missing_image(self):
        """Tests that UserProfileForm accepts submissions with empty image
        field."""

        form = UserProfileForm({'bio': 'Test text bio'}, {'image': ""})
        self.assertTrue(
            form.is_valid(), msg='Form is invalid, but empty image should be accepted')

    def test_form_has_none_image(self):
        """Tests that UserProfileForm accepts submissions with None image
        field."""

        form = UserProfileForm({'bio': 'Test text bio'}, {'image': None})
        self.assertTrue(
            form.is_valid(), msg='Form is invalid, but None image should be accepted')

    def test_form_has_invalid_image(self):
        """Tests that UserProfileForm rejects submissions with invalid image
        content."""

        form = UserProfileForm({'text': 'Test post text'}, {
                               'image': 'invalid_file'})
        self.assertFalse(
            form.is_valid(), msg='Form is valid, but it has an invalid image file')

    def test_form_is_empty(self):
        """Tests that UserProfileForm accepts submissions with no fields."""

        form = UserProfileForm({})
        self.assertTrue(
            form.is_valid(), msg='Form is invalid, but no fields should be accepted')


class TestUserForm(TestCase):
    """Test cases to validate the UserForm model form."""

    def test_form_is_valid(self):
        """Tests that UserForm accepts valid username update."""

        form = UserForm(data={'username': 'test_username'})
        self.assertTrue(form.is_valid(),
                        msg='Form is not valid, but it should be.')

    def test_form_has_invalid_username(self):
        """Tests that UserForm rejects invalid username update."""

        form = UserForm(data={'username': 'test_username*'})
        self.assertFalse(
            form.is_valid(), msg='Form is valid, but the username has an invalid character.')

    def test_form_has_missing_username(self):
        """Tests that UserForm rejects empty username update."""

        form = UserForm(data={'username': ''})
        self.assertFalse(
            form.is_valid(), msg='Form is valid, but the username is missing.')

    def test_form_is_missing_text(self):
        """Tests that UserForm rejects submissions with no data."""

        form = UserForm({})
        self.assertFalse(
            form.is_valid(), msg='Form is valid, but it has no fields.')
