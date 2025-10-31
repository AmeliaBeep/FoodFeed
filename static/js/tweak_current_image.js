let currentImage = document.querySelector("#div_id_image div div");
let imageLink = currentImage.querySelector("a");
let profilePictureUploadInput = document.querySelector("#id_image");
let profilePictureUploadDiv = profilePictureUploadInput.parentElement;


currentImage.innerHTML = `<img class="mx-auto" width=30% src=${imageLink} 
style="border: 1px solid black" 
onerror="this.src='https://res.cloudinary.com/ds7qeovpw/image/upload/v1761573203/foodfeed/no-user-image.jpg'">`;

profilePictureUploadDiv.innerHTML =`
<div class="row"> 
    <div class="col-5">
        <input type="file" name="image" class="form-control" id="id_image">
    </div>

    <div class="col-5">
        <div class="input-group">
            <span class="input-group-text">Remove?</span>
            <div class="form-control">
            <input class="form-check-input" type="checkbox" name="delete_image_toggle" id="delete_image_toggle" value="delete">
            </div>
        </div>
        <label class= for="delete_image_toggle"></label>
    </div>
</div>`;



/*
<div class="row"> 
    <div class="col-6">
        <input type="file" name="image" class="form-control" id="id_image">
    </div>
    <div class="col-6">
        <input type="checkbox" name="delete_image_toggle" id="delete_image_toggle" value="delete">
        <label class= for="delete_image_toggle">Remove profile picture?</label>
    </div>
</div>`;
*/

/*
<span class="input-group-text">Currently</span>

<div class="input-group mb-2"> 
    <span class="input-group-text">Currently</span> 
    <div class="form-control d-flex h-auto">
        <img class="mx-auto" width="30%" src="http://res.cloudinary.com/ds7qeovpw/image/upload/v1761916699/foodfeed/vt9kx5gnyb5jvz1z4amg.png" style="border: 1px solid black" onerror="this.src='https://res.cloudinary.com/ds7qeovpw/image/upload/v1761573203/foodfeed/no-user-image.jpg'">
    </div>
</div>
*/