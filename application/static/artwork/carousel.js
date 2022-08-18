var modal = document.getElementById("myModal");
var modalImg = document.getElementById("modalImg");
var likeCaption = document.getElementById("likeCaption");
var likeButton = document.getElementById("likeButton");
var modalOpen = false;
var imageDictionary = null;
var imgDictLen = 0;
var currentImage = null;
var current_position = 0;
var srcFolder = "../static/images/"
var liked_icon = "../static/images/like-fill-white.png";
var unliked_icon = "../static/images/like-outline.png"
var message_collection = ["Add to your collection", "Added to your collection", "Currently in your collection", "Removed from your collection"];
var deleteButton = document.querySelector('.deleteButton')

document.onkeydown = checkKey;

function triggerModal(caller, img_id, art_type){
  getImages(caller, img_id, art_type)
}

function openModal(caller, img_id){
  imgDictLen = Object.keys(imageDictionary).length

  for(let i = 0; i < imgDictLen; i++){
    if (imageDictionary[i].id == img_id){
      current_position = imageDictionary[i].position;
      break;
    }
  }

  checkLikeStatus()

  modalOpen = true;
  modalImg.src = caller.src;
  if(deleteButton != null){
    deleteButton.setAttribute('data-dbType', 'Artwork')
    deleteButton.setAttribute('data-dbObject', imageDictionary[current_position].id)
  }
  modal.style.display = "flex";
  modal.style.justifyContent = "center";
  modal.style.alignItems = "center";
}

function checkLikeStatus(){
  if(imageDictionary[current_position].isLiked){
    current_img_liked = true;
    likeButton.src = liked_icon;
    likeCaption.innerText = "Currently in your collection"
  }
  else{
    current_img_liked = false;
    likeButton.src = unliked_icon;
    likeCaption.innerText = "Add to your collection"
  }
}

function likeToggle(){
  if(current_img_liked){
    if (message_collection.includes(likeCaption.innerText)){
      likeCaption.innerText = 'Removed from your collection';
    }
    current_img_liked = false;
    imageDictionary[current_position].isLiked = false;
    likeButton.src = unliked_icon;
    updateLikeStatus(imageDictionary[current_position])
  }
  else{
    if (message_collection.includes(likeCaption.innerText)){
      likeCaption.innerText = 'Added to your collection';
    }
    current_img_liked = true;
    imageDictionary[current_position].isLiked = true;
    likeButton.src = liked_icon;
    updateLikeStatus(imageDictionary[current_position])
  }
}

function prevImage(){
  current_position = current_position - 1;

  if(current_position < 0){
    current_position = imgDictLen - 1;
  }

  checkLikeStatus()

  modalImg.src = srcFolder + imageDictionary[current_position].src;
}

function nextImage(){
  current_position = current_position + 1;

  if(current_position >= imgDictLen){
    current_position = 0;
  }

  checkLikeStatus()

  modalImg.src = srcFolder + imageDictionary[current_position].src;
}


function closeModal(){
  modal.style.display = "none";
}

function checkKey(e) {
  if(modalOpen){
   e = e || window.event;

  if (e.key == "ArrowLeft") {
      prevImage();
    }
    else if (e.key == "ArrowRight") {
        nextImage();
    }
    else if (e.key == "Escape"){
      closeModal();
    }
  }
}

function getImages(caller, img_id, art_type){
    jQuery.ajax({ 
         url: "/api/digital-art/" + art_type,
         type: 'GET', 
         timeout: 5000,
         success: function(data) { 
            if (data) {
              imageDictionary = data;
              openModal(caller, img_id)
            }
       }
    })
}

function updateLikeStatus(obj){
  jQuery.ajax({ 
    url: "/api/digital-art/" + art_type,
    type: 'POST', 
    contentType: 'application/json',
    data: JSON.stringify(obj),
    dataType: 'json',
    timeout: 5000,
    success: function(response) { 
      if (response.redirect) {
        window.location.href = response.redirect;
      }
    }
  })
}