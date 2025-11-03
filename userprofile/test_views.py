from django.test import TestCase
from django.urls import reverse
from mainfeed.forms import PostForm
from mainfeed.models import Post
from userprofile.forms import UserForm, UserProfileForm
import cloudinary.api
import requests
from cloudinary.uploader import destroy
from django.core.files.base import ContentFile
from django.db.utils import IntegrityError

class TestUserProfileView(TestCase):

    def setUp(self):
        """ 
        Creates user profile for test cases 
               
        """
        user_profile_form = UserProfileForm({'bio': ''}, None)
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
        response = self.client.get(reverse('user_profile', args=[self.profile_id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_username", response.content)
        self.assertIn(b"no-user-image.jpg", response.content)
        self.assertIn(b"Test post one", response.content)
        self.assertIn(b"Test post two", response.content)

        post_list = self.post_list
        [cloudinary.uploader.destroy(post.image.public_id) for post in post_list]
        