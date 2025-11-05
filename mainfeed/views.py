from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect

from userprofile.models import UserProfile
from .models import Post, Comment
from .forms import PostForm, PostTextForm, CommentForm

# Create your views here.


class PostList(generic.ListView):
    """
    View to list all posts.

    Post objects can be accessed in the template through post_list
    """
    queryset = Post.objects.all()
    template_name = "mainfeed/index.html"
    paginate_by = 10


def create_post(request):
    """
    Handles POST and GET requests related to post creation.

    For POST requests, a new post is added to the database:
        - The post has its image and text fields set according to the form 
        contents included in the request. 
        - The user who submitted the form is set as the author.

    For GET requests, render the webpage for creating posts.

    Args:
        request (HttpRequest): The request to process post creation or to 
        serve the corresponding webpage

    Returns:
        Union[HttpRequest, HttpResponse]:
            - Upon handling a POST request, a redirect request including a 
            success message.
            - Upon handling a GET request, a response containing the page 
            and post create form to render.
    """
    if not request.user.is_authenticated:
        messages.add_message(
            request, messages.INFO,
            'Sign in to create a post!'
        )
        return HttpResponseRedirect(reverse('feed'))

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        try:
            image = request.FILES.get('image')
            content_type = image.content_type
            valid_content = ["image/jpeg", "image/png", "image/svg+xml"]
            if content_type not in valid_content:
                messages.add_message(
                    request, messages.ERROR,
                    'File uploaded not one of the accepted types. Please try uploading an image of JPG, PNG or SVG format'
                )
                raise ValueError(f'File content_type not in ${valid_content}. Instead it was ${content_type}.')
        except (AttributeError, ValueError) as error:
            post_form.add_error('image', error)

        if post_form.is_valid():
            profile_queryset = UserProfile.objects.filter(user=request.user)
            author_profile = get_object_or_404(profile_queryset)
            post = post_form.save(commit=False)
            post.author = author_profile
            post.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Post submitted successfully!'
            )
            return HttpResponseRedirect(reverse('feed'))
        else:
            messages.add_message(
                request, messages.ERROR,
                'Post failed to submit'
            )
            return HttpResponseRedirect(reverse('feed'))
    else:
        post_form = PostForm()
        return render(
            request,
            "mainfeed/create_post.html",
            {
                "post_form": post_form,
            }
        )



def edit_post(request, post_id):
    """
    Handles POST and GET requests related to post editing.

    For POST requests, the target post in the database is updated:
        - The post has its text field set according to the form contents 
        included in the request.

    For GET requests, render the webpage for editing a target post.

    Args:
        request (HttpRequest): The request to process post editing or to 
        serve the corresponding webpage
        post_id (int): The id of the post to edit.


    Returns:
        Union[HttpRequest, HttpResponse]:
            - Upon handling a POST request, a redirect request including a 
            success message.
            - Upon handling a GET request, a response containing the page 
            and the post edit form to render.
    """

    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated or request.user != post.author.user:
        messages.add_message(
            request, messages.ERROR,
            'Not authorised to edit this post!'
        )
        return HttpResponseRedirect(reverse('feed'))

    if request.method == "POST":
        post_form = PostTextForm(request.POST, instance=post)

        if post_form.is_valid() and post.author.user == request.user:
            post = post_form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'Post updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating post!')
        return HttpResponseRedirect(reverse('feed'))

    else:

        post_text_form = PostTextForm(initial={'text': post.text})
        return render(
            request,
            "mainfeed/edit_post.html",
            {
                "post": post,
                "post_text_form": post_text_form,
            },
        )



def delete_post(request, post_id):
    """
    Handles a request to delete a post.

    Args:
        request (HttpRequest): The request to process the deletion.
        post_id (int): The id of the post to delete.

    Returns:
        HttpResponse: a redirect request including a success message.
    """

    post = get_object_or_404(Post, pk=post_id)

    if request.user.is_authenticated and request.user == post.author.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'Not authorised to delete this post!')
    return HttpResponseRedirect(reverse('feed'))




def create_comment(request, post_id):
    """
    Handles POST and GET requests related to comment creation.

    For POST requests, a new comment is added to the database:
        - The comment has its body field set according to the form 
        contents included in the request.
        - The user who submitted the form is set as the author.
        - The comment is linked to its corresponding post.

    For GET requests, render the webpage for creating comments.

    Args:
        request (HttpRequest): The request to process comment creation or to 
        serve the corresponding webpage
        post_id (int): The id of the post associated with the new comment.

    Returns:
        Union[HttpRequest, HttpResponse]:
            - Upon handling a POST request, a redirect request including a 
            success message.
            - Upon handling a GET request, a response containing the page 
            and comment create form to render.
    """
    post = get_object_or_404(Post, pk=post_id)
    if not request.user.is_authenticated:
        messages.add_message(
            request, messages.INFO,
            'Sign in to create a comment!'
        )
        return HttpResponseRedirect(reverse('feed'))

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            queryset = Post.objects.filter(pk=post_id)
            profile_queryset = UserProfile.objects.filter(user=request.user)
            author_profile = get_object_or_404(profile_queryset)
            comment = comment_form.save(commit=False)
            comment.post = get_object_or_404(queryset)
            comment.author = author_profile
            comment.save()
            messages.add_message(
                request, messages.SUCCESS,
                'Comment submitted successfully!'
            )
            return HttpResponseRedirect(reverse('feed'))
        else:
            messages.add_message(
                request, messages.ERROR,
                'Comment failed to submit'
            )
            return HttpResponseRedirect(reverse('feed'))
    else:
        post = get_object_or_404(Post, pk=post_id)

        comment_form = CommentForm()
        return render(
            request,
            "mainfeed/create_comment.html",
            {
                "post": post,
                "comment_form": comment_form,
            },
        )



def edit_comment(request, post_id, comment_id):
    """
    Handles POST and GET requests related to comment editing.

    For POST requests, the target comment in the database is updated:
        - The comment has its body field set according to the form 
        contents included in the request.

    For GET requests, render the webpage for editing a target comment.

    Args:
        request (HttpRequest): The request to process comment editing or to 
        serve the corresponding webpage
        post_id (int): The id of the post associated with the comment.
        comment_id (int): The id of the comment to edit.

    Returns:
        Union[HttpRequest, HttpResponse]:
            - Upon handling a POST request, a redirect request including a 
            success message.
            - Upon handling a GET request, a response containing the page 
            and comment edit form to render.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if not request.user.is_authenticated or request.user != comment.author.user:
        messages.add_message(
            request, messages.ERROR,
            'Not authorised to edit this comment!'
        )
        return HttpResponseRedirect(reverse('feed'))

    if request.method == "POST":
        comment_form = CommentForm(request.POST, instance=comment)

        if comment_form.is_valid() and comment.author.user == request.user:
            comment = comment_form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'Comment updated!')
        else:
            messages.add_message(request, messages.ERROR,
                                 'Error updating comment!')
        return HttpResponseRedirect(reverse('feed'))

    else:
        post = get_object_or_404(Post, pk=post_id)
        comment = get_object_or_404(Comment, pk=comment_id)
        comment_form = CommentForm(initial={'body': comment.body})
        return render(
            request,
            "mainfeed/edit_comment.html",
            {
                "post": post,
                "comment": comment,
                "comment_form": comment_form,
            },
        )



def delete_comment(request, comment_id):
    """
    Handles a request to delete a comment.

    Args:
        request (HttpRequest): The request to process the deletion.
        comment_id (int): The id of the comment to delete.

    Returns:
        HttpResponse: a redirect request including a success message.
    """
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user.is_authenticated and comment.author.user == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'Not authorised to delete this comment!')
    return HttpResponseRedirect(reverse('feed'))