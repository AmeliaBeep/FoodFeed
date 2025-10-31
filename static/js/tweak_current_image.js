let currentImage = document.querySelector("#div_id_image div div");
let imageLink = currentImage.querySelector("a");

currentImage.innerHTML = `<img class="mx-auto" width=30% src=${imageLink} 
style="border: 1px solid black" 
onerror="this.src='https://res.cloudinary.com/ds7qeovpw/image/upload/v1761573203/foodfeed/no-user-image.jpg'">`;



