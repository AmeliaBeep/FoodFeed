from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm, CommentForm

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
                    'Post submitted successfully!'
                )
                return HttpResponseRedirect(reverse('feed'))
            else:
                messages.add_message(
                    request, messages.ERROR,
                    'Post failed to submit'
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