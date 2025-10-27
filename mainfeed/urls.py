from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='feed'),
    path('create-post', views.create_post, name='create_post'),
    path('create-comment/<int:post_id>', views.create_comment, name='create_comment'),
    path('edit-post/<int:post_id>', views.edit_post, name='edit_post'),
]

# urlpatterns = [
#     path('', views.PostList.as_view(), name='home'),
#     path('<slug:slug>/', views.post_detail, name='post_detail'),
#     path('<slug:slug>/edit_comment/<int:comment_id>', views.comment_edit, name='comment_edit'),
#     path('<slug:slug>/delete_comment/<int:comment_id>', views.comment_delete, name='comment_delete'),
# ]