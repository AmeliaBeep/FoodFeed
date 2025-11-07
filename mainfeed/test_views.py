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

from .forms import CommentForm, PostForm, PostTextForm
from .models import Comment, Post


class TestPostView(TestCase):
    """Test cases to validate the view_post view.

    The view is for viewing an individual post."""

    def setUp(self):
        """Creates a user profile and post to be used in test 
        cases."""

        # Create user and update their profile.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

    def test_render_view_post_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        response = self.client.get(
            reverse('view_post', args=[self.post.id]))

        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIsInstance(
            response.context['post'], Post)


class TestCreatePostView(TestCase):
    """Test cases to validate the create_post view."""

    def setUp(self):
        """Creates a user profile to be used in test cases."""

        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unauthenticated users."""

        response = self.client.get(
            reverse('create_post'))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Sign in to create a post!", str(messages[0]))
        self.assertEqual('info', messages[0].level_tag)

    def test_render_create_post_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        self.client.login(
            username="test_user", password="password")
        response = self.client.get(
            reverse('create_post'))
        
        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIsInstance(
            response.context['post_form'], PostForm)

    def test_post_create_success(self):
        """Tests that the view can successfully create a post."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        new_image = SimpleUploadedFile(name="Test image",
                                       content=test_image.content,
                                       content_type="image/jpeg")

        post_data = {
            'text': 'Test post text',
            'image': new_image
        }

        response = self.client.post(
            path=reverse('create_post'), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Verify new values.
        post_made = get_object_or_404(Post, pk=1)
        self.assertEqual('test_user', post_made.author.user.username)
        self.assertEqual('Test post text', post_made.text)
        if not hasattr(post_made.image, 'public_id'):
            self.fail

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Post submitted successfully!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

        cloudinary.uploader.destroy(post_made.image.public_id)

    def test_create_post_invalid_image_rejection(self):
        """Tests that the view won't create a post with an invalid image
        file."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        cloudinary_test_image = cloudinary.api.resource(
            "invalid_content_type_file")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        new_image = SimpleUploadedFile(name="invalid_content_type_file",
                                       content=test_image.content,
                                       content_type="application/pdf")

        post_data = {
            'text': 'Test post text',
            'image': new_image
        }

        response = self.client.post(
            path=reverse('create_post'), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(2, len(messages))
        self.assertEqual(
            "File uploaded not one of the accepted types. Please try uploading an image of JPG, PNG or SVG format.", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag,)
        self.assertEqual("Post failed to submit!", str(messages[1]))
        self.assertEqual('error', messages[1].level_tag,)

        # Verify (no) new values.
        self.assertEqual(0, len(Post.objects.all()))

    def test_create_post_invalid_form_rejection(self):
        """Tests that an invalid form will fail to make a post."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'text': '',
            'image': ''
        }

        response = self.client.post(
            path=reverse('create_post'), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Post failed to submit!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag,)

        # Verify (no) new values.
        self.assertEqual(0, len(Post.objects.all()))


class TestEditPostView(TestCase):
    """Test cases to validate the edit_post view."""

    def setUp(self):
        """Creates a user profile with a post to be used in test cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unauthenticated users."""

        response = self.client.get(
            reverse('edit_post', args=[self.post.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Not authorised to edit this post!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_redirect_if_unauthorised(self):
        """Tests view redirects unauthorised users."""

        User.objects.create_user(
            username="unauthorised_user",
            password="password"
        )

        self.client.login(
            username="unauthorised_user", password="password")

        response = self.client.get(
            reverse('edit_post', args=[self.post.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
    
        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Not authorised to edit this post!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_render_edit_post_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        self.client.login(
            username="test_user", password="password")
        
        response = self.client.get(
            reverse('edit_post', args=[self.post.id]))

        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIn(self.post.text.encode(
            'UTF-8'), response.content)
        self.assertIsInstance(
            response.context['post'], Post)
        self.assertIsInstance(
            response.context['post_text_form'], PostTextForm)

    def test_edit_post_success(self):
        """Tests that the view can successfully edit a post."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'text': 'Test edited post text',
        }

        response = self.client.post(
            path=reverse('edit_post', args=[self.post.id]), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Verify new values.
        post_edited = get_object_or_404(Post, pk=1)
        self.assertEqual('Test edited post text', post_edited.text)

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Post updated!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

    def test_edit_post_invalid_form_rejection(self):
        """Tests that an invalid form will fail to edit the post."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'text': ''
        }

        response = self.client.post(
            path=reverse('edit_post', args=[self.post.id]), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Error updating post!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag,)

        # Verify (no) new values.
        post_edited = get_object_or_404(Post, pk=1)
        self.assertNotEqual('', post_edited.text)

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""

        cloudinary.uploader.destroy(
            self.post.image.public_id)


class TestDeletePostView(TestCase):
    """Test cases to validate the delete_post view."""

    def setUp(self):
        """Creates a user profile with a post to be used in test cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unauthenticated users."""

        response = self.client.get(
            reverse('delete_post', args=[self.post.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to delete this post!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_redirect_if_unauthorised(self):
        """Tests view redirects unauthorised users."""

        User.objects.create_user(
            username="unauthorised_user",
            password="password"
        )

        self.client.login(
            username="unauthorised_user", password="password")

        response = self.client.get(
            reverse('delete_post', args=[self.post.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to delete this post!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_delete_post_success(self):
        """Tests that the view can successfully delete a post."""

        self.client.login(
            username="test_user", password="password")

        response = self.client.post(
            path=reverse('delete_post', args=[self.post.id]))
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Post deleted!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag,)

        # Verify deletion.
        self.assertEqual(0, len(Post.objects.all()))

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""

        cloudinary.uploader.destroy(
            self.post.image.public_id)


class TestCommentView(TestCase):
    """Test cases to validate the view_comment view.

    The view is for viewing an individual comment."""

    def setUp(self):
        """Creates a user profile and post and comment to be used 
        in test cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

        # Create test comment.
        self.comment = Comment.objects.create(
            body='Test comment text',
            post=self.post,
            author=self.test_user_profile
        )

    def test_render_view_comment_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        response = self.client.get(
            reverse('view_comment', args=[self.post.id, self.comment.id]))

        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIsInstance(
            response.context['post'], Post)
        self.assertIsInstance(
            response.context['comment'], Comment)


class TestCreateCommentView(TestCase):
    """Test cases to validate the create_comment view."""

    def setUp(self):
        """Creates a user profile with a post to be used in test cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unauthenticated users."""

        response = self.client.get(
            reverse('create_comment', args=[self.post.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Sign in to create a comment!", str(messages[0]))
        self.assertEqual('info', messages[0].level_tag)

    def test_render_create_comment_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        self.client.login(
            username="test_user", password="password")
        
        response = self.client.get(
            reverse('create_comment', args=[self.post.id]))

        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIsInstance(
            response.context['post'], Post)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

    def test_comment_create_success(self):
        """Tests that the view can successfully create a comment."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'body': 'Test comment text'
        }

        response = self.client.post(
            path=reverse('create_comment', args=[self.post.id]), data=post_data)
        

        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Verify new values.
        comment_made = get_object_or_404(Comment, pk=1)
        self.assertEqual('test_user', comment_made.author.user.username)
        self.assertEqual('Test comment text', comment_made.body)

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Comment submitted successfully!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

    def test_create_comment_invalid_form_rejection(self):
        """Tests that an invalid form will fail to make a comment."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'body': '',
        }

        response = self.client.post(
            path=reverse('create_comment', args=[self.post.id]), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Comment failed to submit!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag,)

        # Verify (no) new values.
        self.assertEqual(0, len(Comment.objects.all()))

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""

        cloudinary.uploader.destroy(
            self.post.image.public_id)


class TestEditCommentView(TestCase):
    """Test cases to validate the edit_comment view."""

    def setUp(self):
        """Creates a user profile with a post and comment to be used in test
        cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

        # Create test comment.
        self.comment = Comment.objects.create(
            body='Test comment text',
            post=self.post,
            author=self.test_user_profile
        )

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unauthenticated users."""

        response = self.client.get(
            reverse('edit_comment', args=[self.post.id, self.comment.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to edit this comment!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_redirect_if_unauthorised(self):
        """Tests view redirects unauthorised users."""

        User.objects.create_user(
            username="unauthorised_user",
            password="password"
        )

        self.client.login(
            username="unauthorised_user", password="password")

        response = self.client.get(
            reverse('edit_comment', args=[self.post.id, self.comment.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to edit this comment!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_render_edit_post_page(self):
        """Tests the page renders successfully and includes expected
        content."""

        self.client.login(
            username="test_user", password="password")
        
        response = self.client.get(
            reverse('edit_comment', args=[self.post.id, self.comment.id]))

        # Check response.
        self.assertEqual(response.status_code, 200)

        # Check content rendered.
        self.assertIsInstance(
            response.context['post'], Post)
        self.assertIsInstance(
            response.context['comment'], Comment)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

    def test_edit_comment_success(self):
        """Tests that the view can successfully edit a comment."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'body': 'Test edited comment text',
        }

        response = self.client.post(
            path=reverse('edit_comment', args=[self.post.id, self.comment.id]), data=post_data)
        
        # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Verify new values.
        comment_edited = get_object_or_404(Comment, pk=1)
        self.assertEqual('Test edited comment text', comment_edited.body)

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Comment updated!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag)

    def test_edit_comment_invalid_form_rejection(self):
        """Tests that an invalid form will fail to edit the comment."""

        self.client.login(
            username="test_user", password="password")

        # Set up details and then make the post request.
        post_data = {
            'body': ''
        }

        response = self.client.post(
            path=reverse('edit_comment', args=[self.post.id, self.comment.id]), data=post_data)
       
       # Check response.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Error updating comment!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag,)

        # Verify (no) new values.
        comment_edited = get_object_or_404(Comment, pk=1)
        self.assertNotEqual('', comment_edited.body)

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""

        cloudinary.uploader.destroy(
            self.post.image.public_id)


class TestDeleteCommentView(TestCase):
    """Test cases to validate the delete_comment view."""

    def setUp(self):
        """Creates a user profile with a post and comment to be used in test
        cases."""

        # Create user for tests.
        self.test_user = User.objects.create_user(
            username="test_user",
            password="password"
        )
        self.test_user_profile = self.test_user.user_profile

        # Get test image and create image object for test post.
        cloudinary_test_image = cloudinary.api.resource("test_image")
        test_image_url = cloudinary_test_image.get('url')
        test_image = requests.get(test_image_url)
        test_image_content = ContentFile(test_image.content)
        test_image_content.name = 'test_image.jpg'
        image = {'image': test_image_content}

        # Create test post.
        post_form = PostForm({'text': 'Test post text'}, image)
        post = post_form.save(commit=False)
        post.author = self.test_user_profile
        post.save()
        self.post = post

        # Create test comment.
        self.comment = Comment.objects.create(
            body='Test comment text',
            post=self.post,
            author=self.test_user_profile
        )

    def test_redirect_if_unauthenticated(self):
        """Tests view redirects unathenticated users."""

        response = self.client.get(
            reverse('delete_comment', args=[self.comment.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to delete this comment!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_redirect_if_unauthorised(self):
        """Tests view redirects unathorised users."""

        User.objects.create_user(
            username="unauthorised_user",
            password="password"
        )

        self.client.login(
            username="unauthorised_user", password="password")

        response = self.client.get(
            reverse('delete_comment', args=[self.comment.id]))
        
        # Check redirect.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual(
            "Not authorised to delete this comment!", str(messages[0]))
        self.assertEqual('error', messages[0].level_tag)

    def test_delete_comment_success(self):
        """Tests that the view can successfully delete a comment."""

        self.client.login(
            username="test_user", password="password")

        response = self.client.post(
            path=reverse('delete_comment', args=[self.comment.id]))
        
        # Check response.
        self.assertEqual(response.status_code, 302)

        # Check messages provided to user.
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(1, len(messages))
        self.assertEqual("Comment deleted!", str(messages[0]))
        self.assertEqual('success', messages[0].level_tag,)

        # Verify deletion.
        self.assertEqual(0, len(Comment.objects.all()))

    def tearDown(self):
        """Deletes Cloudinary resources uploaded during testing."""

        cloudinary.uploader.destroy(
            self.post.image.public_id)
