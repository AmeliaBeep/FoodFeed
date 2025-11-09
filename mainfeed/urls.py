from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='feed'),
    path('create-post', views.create_post, name='create_post'),
    path('create-comment/<int:post_id>',
         views.create_comment, name='create_comment'),
    path('edit-post/<int:post_id>', views.edit_post, name='edit_post'),
    path('view-post/<int:post_id>/edit-comment/<int:comment_id>',
         views.edit_comment, name='edit_comment'),
    path('delete-post/<int:post_id>', views.delete_post, name='delete_post'),
    path('delete-comment/<int:comment_id>',
         views.delete_comment, name='delete_comment'),
    path('view-post/<int:post_id>', views.view_post, name='view_post'),
    path('view-post/<int:post_id>/view-comment/<int:comment_id>',
         views.view_comment, name='view_comment'),
]
