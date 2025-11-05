import cloudinary.api
import requests
from cloudinary.uploader import destroy
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from mainfeed.forms import PostForm
from mainfeed.models import Post

from userprofile.forms import UserForm, UserProfileForm
from userprofile.models import UserProfile


class TestUserProfileView(TestCase):
    """Test cases to validate the view_user_profile view."""

    def setUp(self):
        """Creates a user profile with two posts to be used in test cases."""

        user_profile_form = UserProfileForm({'bio': 'Test bio'}, None)
        user_form = UserForm(data={'username': 'test_username'})

        self.user = user_form.save()

        user_profile = user_profile_form.save(commit=False)
        user_profile.user = self.user

        user_profile.save()
        self.user_profile = user_profile
        self.profile_id = user_profile.id

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        test_image_content_2 = ContentFile(test_image.content)
        test_image_content_2.name = 'test_image.jpg'

        image = {'image': test_image_content}
        image2 = {'image': test_image_content_2}

        post_form_1 = PostForm({'text': 'Test post one'}, image)
        post_1 = post_form_1.save(commit=False)
        post_1.author = self.user_profile
        post_1.save()

        post_form_2 = PostForm({'text': 'Test post two'}, image2)
        post_2 = post_form_2.save(commit=False)
        post_2.author = self.user_profile
        post_2.save()

        self.post_list = Post.objects.all()

    def test_render_page(self):
        """Tests the page renders successfully and includes expected content.

        The test user profile has no profile picture which should result
        in the default no-user-image file being used and rendered.
        """

        response = self.client.get(
            reverse('user_profile', args=[self.profile_id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_username", response.content)
        self.assertIn(b"no-user-image.jpg", response.content)
        self.assertIn(b"Test bio", response.content)
        self.assertIn(b"Test post one", response.content)
        self.assertIn(b"Test post two", response.content)

        post_list = self.post_list
        [cloudinary.uploader.destroy(post.image.public_id)
         for post in post_list]


class TestUserProfileEditView(TestCase):
    """Test cases to validate the edit_user_profile view."""

    def setUp(self):
        """Creates two user profile for test cases.

        One test profile has no bio and image, but the second has a bio
        and profile set.
        """
        # User with a blank bio and no uploaded image
        self.user_no_bio_image = User.objects.create_user(
            username="test_no_bio_or_image",
            password="password"
        )

        user_profile_form_no_bio_image = UserProfileForm({'bio': ''}, None)
        user_profile_no_bio_image = user_profile_form_no_bio_image.save(
            commit=False)
        user_profile_no_bio_image.user = self.user_no_bio_image

        user_profile_no_bio_image.save()
        self.user_profile_no_bio_image = user_profile_no_bio_image
        self.profile_id_no_bio_image = user_profile_no_bio_image.id

        # User with a set bio and uploaded image
        self.user_set_bio_image = User.objects.create_user(
            username="test_set_bio_or_image",
            password="password"
        )

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')

        test_image = requests.get(test_image_url)

        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'

        image = {'image': test_image_content}

        user_profile_form_set_bio_image = UserProfileForm(
            {'bio': 'Test bio text'}, image)

        user_profile_set_bio_image = user_profile_form_set_bio_image.save(
            commit=False)
        user_profile_set_bio_image.user = self.user_set_bio_image

        user_profile_set_bio_image.save()
        self.user_profile_set_bio_image = user_profile_set_bio_image
        self.profile_id_set_bio_image = user_profile_set_bio_image.id

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unathenticated users."""

        response = self.client.get(
            reverse('edit_user_profile', args=[self.profile_id_no_bio_image]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/1")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Unauthorised to edit this profile!",
                         str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_redirect_if_unauthorised(self):
        """Tests view redirects unathorised users."""

        self.client.login(
            username="test_set_bio_or_image", password="password")
        response = self.client.get(
            reverse('edit_user_profile', args=[self.profile_id_no_bio_image]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/1")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Unauthorised to edit this profile!",
                         str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_render_page_with_no_bio_or_image(self):
        """Tests the page renders successfully and includes expected content.

        The view should present a page with a profile edit form with
        fields to edit the username, profile picture and bio. Any pre-
        existing values for these fields should be shown to the user.

        The test user profile used has no profile picture, which should
        result in the no-profile-image file being used and rendered.
        """

        self.client.login(
            username="test_no_bio_or_image", password="password")
        response = self.client.get(
            reverse('edit_user_profile', args=[self.profile_id_no_bio_image]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_profile_no_bio_image.user.username.encode(
            'UTF-8'), response.content)
        # self.assertIn(self.user_profile_no_bio_image.image.url.encode('UTF-8'), response.content)
        self.assertIn(b'no-profile-image', response.content)
        self.assertIn(
            b'<textarea name="bio" cols="40" rows="10" maxlength="800" class="textarea form-control" id="id_bio">\n</textarea>', response.content)
        self.assertIsInstance(
            response.context['user_form'], UserForm)
        self.assertIsInstance(
            response.context['user_profile_form'], UserProfileForm)

    def test_render_page_with_set_bio_or_image(self):
        """Tests the page renders successfully and includes expected content.

        The view should present a page with a profile edit form with
        fields to edit the username, profile picture and bio. Any pre-
        existing values for these fields should be shown to the user.

        The test user profile has a profile picture which should result
        in the test image file being used and rendered.
        """

        self.client.login(
            username="test_set_bio_or_image", password="password")
        response = self.client.get(
            reverse('edit_user_profile', args=[self.profile_id_set_bio_image]))

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user_profile_set_bio_image.user.username.encode(
            'UTF-8'), response.content)
        self.assertIn(self.user_profile_set_bio_image.image.url.encode(
            'UTF-8'), response.content)
        self.assertIn(self.user_profile_set_bio_image.bio.encode(
            'UTF-8'), response.content)
        self.assertIsInstance(
            response.context['user_form'], UserForm)
        self.assertIsInstance(
            response.context['user_profile_form'], UserProfileForm)

    def test_profile_edits_update_all_success(self):
        """Tests that the view can successfully update the user profile when
        provided valid changes from an authorised user."""

        self.client.login(
            username="test_no_bio_or_image", password="password")

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        new_image = SimpleUploadedFile(name="new profile image",
                                       content=test_image.content,
                                       content_type="image/jpeg")

        post_data = {
            'username': 'new_username',
            'bio': 'new test bio',
            'image': new_image
        }

        response = self.client.post(
            path=reverse('edit_user_profile', args=[self.profile_id_no_bio_image]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/1")

        profile = get_object_or_404(
            UserProfile, pk=self.profile_id_no_bio_image)
        self.assertEqual('new_username', profile.user.username)
        self.assertEqual('new test bio', profile.bio)
        self.assertNotEqual('no-profile-image', profile.image)
        if not hasattr(profile.image, 'public_id'):
            self.fail

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Profile updated!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

    def test_profile_edits_no_update(self):
        """Tests that the view can does not update the user profile when
        provided no changes from an authorised user."""

        self.client.login(
            username="test_set_bio_or_image", password="password")

        post_data = {
            'username': self.user_profile_set_bio_image.user.username,
            'bio': self.user_profile_set_bio_image.bio,
            'image': ''
        }

        response = self.client.post(
            path=reverse('edit_user_profile', args=[self.profile_id_set_bio_image]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/2")

        profile = get_object_or_404(
            UserProfile, pk=self.profile_id_set_bio_image)
        self.assertEqual(
            self.user_profile_set_bio_image.user.username, profile.user.username)
        self.assertEqual(self.user_profile_set_bio_image.bio, profile.bio)
        self.assertEqual(
            self.user_profile_set_bio_image.image.public_id, profile.image.public_id)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(0, len(messages))

    def test_profile_edits_empty_username_rejection(self):
        """Test that username cannot be updated to be empty."""

        self.client.login(
            username="test_set_bio_or_image", password="password")

        post_data = {
            'username': ''
        }
        response = self.client.post(
            path=reverse('edit_user_profile', args=[self.profile_id_set_bio_image]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/2")

        profile = get_object_or_404(
            UserProfile, pk=self.profile_id_set_bio_image)
        self.assertNotEqual('', profile.user.username)
        self.assertEqual(
            self.user_profile_set_bio_image.user.username, profile.user.username)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Error updating profile!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

        for message in messages:
            print(f"Message: {message}, Level: {message.level_tag}")

    def test_profile_edits_invalid_image_rejection(self):
        """Test that image file can only be of JPG, PNG or SVG types."""

        self.client.login(
            username="test_set_bio_or_image", password="password")

        cloudinary_test_image = cloudinary.api.resource(
            "invalid_content_type_file")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        new_image = SimpleUploadedFile(name="invalid_content_type_file",
                                       content=test_image.content,
                                       content_type="application/pdf")

        post_data = {
            'username': self.user_profile_set_bio_image.user.username,
            'bio': self.user_profile_set_bio_image.bio,
            'image': new_image
        }
        response = self.client.post(
            path=reverse('edit_user_profile', args=[self.profile_id_set_bio_image]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/2")

        profile = get_object_or_404(
            UserProfile, pk=self.profile_id_set_bio_image)
        self.assertEqual(
            self.user_profile_set_bio_image.image.public_id, profile.image.public_id)

        messages = list(get_messages(response.wsgi_request))
        for message in messages:
            print(f"Message: {message}, Level: {message.level_tag}")
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "File uploaded not one of the accepted types. Please try uploading an image of JPG, PNG or SVG format. No changes made to profile picture.", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_profile_edits_delete_image_success(self):
        """Test that the user profile image is removed when the request has the
        delete_image_toggle option checked.

        Also that any image submitted is ignored and not saved.
        """

        self.client.login(
            username="test_set_bio_or_image", password="password")

        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        new_image = SimpleUploadedFile(name="new profile image",
                                       content=test_image.content,
                                       content_type="image/jpeg")

        post_data = {
            'username': self.user_profile_set_bio_image.user.username,
            'bio': self.user_profile_set_bio_image.bio,
            'delete_image_toggle': 'True',
            'image': new_image
        }

        response = self.client.post(
            path=reverse('edit_user_profile', args=[self.profile_id_set_bio_image]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/user-profile/2")

        profile = get_object_or_404(
            UserProfile, pk=self.profile_id_set_bio_image)
        self.assertNotEqual(
            str(self.user_profile_set_bio_image.image), str(profile.image))
        self.assertEqual('no-profile-image', str(profile.image))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Profile updated!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""
        
        cloudinary.uploader.destroy(
            self.user_profile_set_bio_image.image.public_id)
