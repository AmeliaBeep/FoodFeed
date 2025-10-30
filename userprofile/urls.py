from . import views
from django.urls import path

urlpatterns = [
    path('user-profile', views.user_profile, name='user_profile'),
]