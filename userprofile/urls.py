from django.urls import path

from . import views

urlpatterns = [
    path('user-profile/<int:user_profile_id>',
         views.view_user_profile, name='user_profile'),
    path('user-profile/<int:user_profile_id>/edit',
         views.edit_user_profile, name='edit_user_profile'),
]
