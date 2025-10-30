from django.shortcuts import get_object_or_404, render, reverse
from userprofile.models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.


def user_profile(request, user_profile_id):
    profile = get_object_or_404(UserProfile, pk=user_profile_id)

    users_posts = profile.users_posts.all()

    return render(
        request,
        "userprofile/profile.html",
        {
            "profile": profile,
            "posts": users_posts,
        },
    )

def edit_user_profile(request, user_profile_id):
    profile = get_object_or_404(UserProfile, pk=user_profile_id)

    if not request.user.is_authenticated or request.user != profile.user:
        messages.add_message(
            request, messages.ERROR,
            'Unauthorised to edit this profile!'
        )
        return HttpResponseRedirect(reverse('feed'))
    
    user_profile_form = UserProfileForm()

    return render(
        request,
        "userprofile/edit_profile.html",
        {
            "profile": profile,
            "user_profile_form": user_profile_form,
        },
    )
