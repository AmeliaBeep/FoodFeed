from django.shortcuts import get_object_or_404, render, reverse
from userprofile.models import UserProfile
from .forms import UserProfileForm, UserForm
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
    if request.method == "POST":
        post_form = UserForm(request.POST, request.FILES)
        if post_form.is_valid():
            profile_queryset = UserProfile.objects.filter(user=request.user)
            author_profile = get_object_or_404(profile_queryset)
            post = post_form.save(commit=False)
            post.author = author_profile
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
        current_bio = profile.bio
        current_image = profile.image
        username = request.user.username

        user_profile_form = UserProfileForm(
            initial={'bio': current_bio, 'image': current_image})
        user_form = UserForm(initial={'username': username})

        return render(
            request,
            "userprofile/edit_profile.html",
            {
                "profile": profile,
                "user_profile_form": user_profile_form,
                "user_form": user_form,
            },
        )
