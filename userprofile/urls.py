from . import views
from django.urls import path

urlpatterns = [
    path('user-profile/<int:user_profile_id>', views.user_profile, name='user_profile'),
    path('user-profile/<int:user_profile_id>/edit', views.edit_user_profile, name='edit_user_profile'),
]