from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse
from mainfeed.forms import PostForm
from mainfeed.models import Post
from mainfeed.views import PostList
from userprofile.forms import UserForm, UserProfileForm
import cloudinary.api
import requests
from cloudinary.uploader import destroy
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.views import generic

from .models import Post, Comment
from .forms import PostForm, PostTextForm, CommentForm

class TestCreatePostView(TestCase):
    """"""
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )

        user_profile_form_no_bio_image = UserProfileForm({'bio': ''}, None)
        test_user_profile = user_profile_form_no_bio_image.save(
            commit=False)
        test_user_profile.user = self.test_user

        test_user_profile.save()
        self.test_user_profile = test_user_profile

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unathenticated users"""

        response = self.client.get(
            reverse('create_post'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_render_create_post_page(self):
        """"""
        self.client.login(
            username="test_user", password="password")
        response = self.client.get(
            reverse('create_post'))
        
        self.assertIsInstance(
            response.context['post_form'], PostForm)

