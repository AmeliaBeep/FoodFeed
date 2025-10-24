from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Post, Comment
from .forms import PostForm

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.all()
    template_name = "mainfeed/index.html"
    paginate_by = 2

# from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
# def index(request):
#     return HttpResponse("Hello, World!")

def create_post(request):

    if request.method == "POST":
        post_form = PostForm(data=request.POST)
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


# def create_comment(request, post_id):
#     queryset = Post.objects.all()
#     post = get_object_or_404(queryset, pk=post_id)

#     return render(
#         request,
#         "mainfeed/create_post.html",
#         {
#             "post": post,
#         },
#     )