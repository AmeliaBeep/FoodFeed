from django.test import TestCase
from .forms import PostForm, PostTextForm, CommentForm
import cloudinary.api
from django.core.files.base import ContentFile
import requests
from cloudinary.uploader import destroy


class TestPostForm(TestCase):
    """
    Test cases to validate the PostForm model form.
    """

    # TODO: Mock Cloudinary response in creating test_image
    #       Prevent PostForm to_python subroutines from uploading test_image     
    def test_form_is_valid(self):
        """ 
        Tests that PostForm accepts valid text and image fields.

        The valid image is sourced from an existing test_image asset 
        hosted on Cloudinary.

        After a successful test the image uploaded to Cloudinary during
        form object creation is then deleted.
        """
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')

        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}

        form = PostForm({'text': 'Test post text'}, image)

        self.assertTrue(form.is_valid(), msg='Form is not valid, but it should be')

        uploaded_asset_id = form.cleaned_data['image'].public_id
        cloudinary.uploader.destroy(uploaded_asset_id)
    
    def test_form_is_missing_text(self):
        """ Tests that PostForm rejects submissions with empty text field."""
        form = PostForm({'text': '', 'image': 'static\images\default.jpg'})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no text')

    def test_form_is_missing_image(self):
        """ Tests that PostForm rejects submissions with empty image field."""
        form = PostForm({'text': 'Test post text', 'image': ''})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no image')
    
    def test_form_has_invalid_image(self):
        """ Tests that PostForm rejects submissions with invalid image content."""
        form = PostForm({'text': 'Test post text', 'image':'invalid_image_file'})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has an invalid image file')

    def test_form_is_empty(self):
        """ Tests that PostForm rejects submissions with no fields."""
        form = PostForm({})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no fields')


class TestPostTextForm(TestCase):
    """
    Test cases to validate the PostTextForm model form.
    """

    def test_form_is_valid(self):
        """Tests that PostTextForm accepts valid text content."""
        form = PostTextForm({'text': 'Test post text'})
        self.assertTrue(form.is_valid(), msg='Form is not valid, but it should be')
    
    def test_form_is_missing_text(self):
        """Tests that PostTextForm rejects submissions with empty text field."""
        form = PostTextForm({'text': ''})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no text')

    def test_form_is_empty(self):
        """Tests that PostTextForm rejects submissions with no fields."""
        form = PostTextForm({})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no fields')


class TestCommentForm(TestCase):
    """
    Test cases to validate the CommentForm model form.
    """

    def test_form_is_valid(self):
        """Tests that CommentForm accepts valid comment body text."""
        form = CommentForm({'body': 'Test comment text'})
        self.assertTrue(form.is_valid(), msg='Form is not valid, but it should be')
    
    def test_form_is_missing_text(self):
        """Tests that CommentForm rejects submissions with empty body field."""
        form = CommentForm({'body': ''})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no body')

    def test_form_is_empty(self):
        """Tests that CommentForm rejects submissions with no fields."""
        form = CommentForm({})
        self.assertFalse(form.is_valid(), msg='Form is valid, but it has no fields')