from django.shortcuts import get_object_or_404, render, reverse
from userprofile.models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
#from magic.identify import Magic, MagicError

# Create your views here.


def view_user_profile(request, user_profile_id):
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

#TODO make it so you get booted out if no changes?
def edit_user_profile(request, user_profile_id):
    profile = get_object_or_404(UserProfile, pk=user_profile_id)

    if not request.user.is_authenticated or request.user != profile.user:
        messages.add_message(
            request, messages.ERROR,
            'Unauthorised to edit this profile!'
        )
        return HttpResponseRedirect(reverse('feed'))
    
    if request.method == "POST":
        handle_user_profile_edits(request, profile)
        return HttpResponseRedirect(reverse('feed'))
    else:
        current_bio = profile.bio
        current_image = profile.image
        username = request.user.username

        user_profile_form = UserProfileForm(initial={'bio': current_bio, 'image': current_image})
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

# TODO: use magic library to properly verify uploaded file is an image
    #filetype_fromname = Magic.id_filename(image)
    #filetype_frombuffer = Magic.id_buffer(image)
def handle_user_profile_edits(request, profile):
    try:
        image = request.FILES.get('image')
        content_type=image.content_type
        valid_content = ["image/jpeg", "image/png", "image/svg+xml"]
        if content_type not in valid_content:
            raise ValueError
        
    except AttributeError:
        image = None

    except ValueError:
        image = None
        messages.add_message(
            request, messages.ERROR,
            'File uploaded not one of the accepted types'
        )

    bio = request.POST.get('bio')
    username = request.POST.get('username')    
    user_profile_form = UserProfileForm(data={'bio':bio}, files={'image':image}, instance=profile)
    user_form = UserForm(data={'username':username}, instance=profile.user)

    if user_profile_form.is_valid() and user_form.is_valid():
        profile = user_profile_form.save(commit=False)
        temp=profile.image
        assert False
        user = user_form.save(commit=True)
        messages.add_message(
            request, messages.SUCCESS,
            'Updates submitted successfully!'
        )
    else:
        messages.add_message(
            request, messages.ERROR,
            'Post failed to submit'
        )