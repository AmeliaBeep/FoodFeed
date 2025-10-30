from django.shortcuts import get_object_or_404, render

from userprofile.models import UserProfile

# Create your views here.


def user_profile(request):
    profile_queryset = UserProfile.objects.filter(user=request.user)
    profile = get_object_or_404(profile_queryset)

    users_posts = profile.users_posts.all()

    return render(
        request,
        "userprofile/profile.html",
        {
            "profile": profile,
            "posts": users_posts,
        },
    )
