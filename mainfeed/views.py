from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, PostTextForm, CommentForm

from cloudinary.uploader import upload_image
# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "mainfeed/index.html"
    paginate_by = 10

# from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
# def index(request):
#     return HttpResponse("Hello, World!")

def create_post(request):

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
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
    else:
        post_form = PostForm()
        return render(
            request,
            "mainfeed/create_post.html",
            {
                "post_form": post_form,
            }
        )


def create_comment(request, post_id):

    if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                queryset = Post.objects.filter(pk=post_id)
                comment.post =  get_object_or_404(queryset)
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
    else:    
        queryset = Post.objects.filter(pk=post_id)
        post = get_object_or_404(queryset)

        comment_form = CommentForm() 
        return render(
            request,
            "mainfeed/create_comment.html",
            {
                "post": post,
                "comment_form": comment_form,
            },
        )
    
def edit_post(request, post_id):
    
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        post_form = PostTextForm(request.POST, instance=post)

        if post_form.is_valid() and post.author == request.user:
            post = post_form.save(commit=True)
            messages.add_message(request, messages.SUCCESS, 'Post Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating post!')
        return HttpResponseRedirect(reverse('feed'))

    else:    
        queryset = Post.objects.filter(pk=post_id)
        post = get_object_or_404(queryset)

        post_text_form = PostTextForm()
        return render(
            request,
            "mainfeed/edit_post.html",
            {
                "post": post,
                "post_text_form": post_text_form,
            },
        )
    
# def edit_comment(request, comment_id):
    
#     if request.method == "POST":
#         post = get_object_or_404(Post, pk=post_id)
#         post_form = PostTextForm(request.POST, instance=post)

#         if post_form.is_valid() and post.author == request.user:
#             post = post_form.save(commit=True)
#             messages.add_message(request, messages.SUCCESS, 'Post Updated!')
#         else:
#             messages.add_message(request, messages.ERROR, 'Error updating post!')
#         return HttpResponseRedirect(reverse('feed'))

#     else:    
#         queryset = Post.objects.filter(pk=post_id)
#         post = get_object_or_404(queryset)

#         post_text_form = PostTextForm()
#         return render(
#             request,
#             "mainfeed/edit_post.html",
#             {
#                 "post": post,
#                 "post_text_form": post_text_form,
#             },
#         )

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author == request.user:
        post.delete()
        messages.add_message(request, messages.SUCCESS, 'Post Deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'Error deleting post!')
    return HttpResponseRedirect(reverse('feed'))

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment Deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'Error deleting comment!')
    return HttpResponseRedirect(reverse('feed'))