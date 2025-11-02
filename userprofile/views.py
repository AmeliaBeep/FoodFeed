from django.shortcuts import get_object_or_404, render, reverse
from userprofile.models import UserProfile
from .forms import UserProfileForm, UserForm
from django.contrib import messages
from django.http import HttpResponseRedirect
# from magic.identify import Magic, MagicError

# Create your views here.


def view_user_profile(request, user_profile_id):
    """
    Handles POST and GET requests related to profile editing.

    For POST requests, the request is processed by handle_user_profile_edits:

    For GET requests, render the webpage for editing the profile.

    Args:
        request (HttpRequest): The request to process user profile editing or to 
        serve the corresponding webpage.
        user_profile_id (int): The id of the user profile to edit.


    Returns:
        (HttpResponse): a response containing the profile page to render.
    """

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

# TODO make it so you get booted out if no changes?


def edit_user_profile(request, user_profile_id):
    """
    Handles POST and GET requests related to profile editing.

    For POST requests, the request is processed by handle_user_profile_edits:

    For GET requests, render the webpage for editing the profile.

    Args:
        request (HttpRequest): The request to process user profile editing or to 
        serve the corresponding webpage.
        user_profile_id (int): The id of the user profile to edit.


    Returns:
        Union[HttpRequest, HttpResponse]:
            - Upon handling a POST request, a redirect request including a 
            success message.
            - Upon handling a GET request, a response containing the page 
            and the profile edit form to render.
    """

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


def handle_user_profile_edits(request, profile):
    """
    Handles the request data provided to edit the user profile.

    The values for the bio and image, corresponding to the UserProfileForm, 
    and the username, corresponding to the UserForm, respectively are 
    retrieved. If these indicate no changes were made then the routine returns.

    The image value is determined by handle_set_image to set the image 
    depending on the delete_image_toggle and if a file was submitted. 
    If remove_image_checked is True then the image will be set to the default placeholder.

    Any valid changes found will be saved to the corresponding profile via saving
    of the respective form objects. The UserProfile includes a key to the
    corresponding User.


    Args:
        request (HttpRequest): The request to process user profile edits.
        user_profile_id (int): The id of the user profile to edit.


    Returns:
        (None)
    """

    remove_image_checked = request.POST.get('delete_image_toggle', False)

    image = handle_set_image(request, remove_image_checked)
    bio = request.POST.get('bio')
    username = request.POST.get('username')

    no_changes_made = image == None and not remove_image_checked and bio == profile.bio and username == profile.user.username

    if no_changes_made:
        return

    user_profile_form = UserProfileForm(
        data={'bio': bio}, files={'image': image}, instance=profile)
    user_form = UserForm(data={'username': username}, instance=profile.user)

    if user_profile_form.is_valid() and user_form.is_valid():
        profile = user_profile_form.save(commit=False)
        if remove_image_checked:
            profile.image = 'no-profile-image'
        profile.save()
        user_form.save(commit=True)
        messages.add_message(
            request, messages.SUCCESS,
            'Updates submitted successfully!'
        )
    else:
        messages.add_message(
            request, messages.ERROR,
            'Post failed to submit'
        )

# TODO: use magic library to properly verify uploaded file is an image
    # filetype_fromname = Magic.id_filename(image)
    # filetype_frombuffer = Magic.id_buffer(image)


def handle_set_image(request, remove_image_checked):
    """
    Gets the valid submitted image or returns none.

    Valid image types are determined by the content-type property
    included in the request. Invalid file types are ignored and None is
    returned instead.

    Args:
        request (HttpRequest): The request to process user profile edits.
        remove_image_checked (bool): The id of the user profile to edit.


    Returns:
        Union[MultiValueDict, None]:
            - The image file of valid content-type
            - None if no changes were found.
    """

    if remove_image_checked:
        return None

    try:
        image = request.FILES.get('image')
        content_type = image.content_type
        valid_content = ["image/jpeg", "image/png", "image/svg+xml"]
        if content_type not in valid_content:
            raise ValueError
    except AttributeError:
        image = None
    except ValueError:
        image = None
        messages.add_message(
            request, messages.ERROR,
            'File uploaded not one of the accepted types. No changes made to profile picture'
        )

    return image
