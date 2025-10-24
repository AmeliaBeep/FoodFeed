from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post, Comment

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