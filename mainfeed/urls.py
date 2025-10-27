from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='feed'),
    path('create-post', views.create_post, name='create_post'),
    path('create-comment/<int:post_id>', views.create_comment, name='create_comment'),
    path('edit-post/<int:post_id>', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
]