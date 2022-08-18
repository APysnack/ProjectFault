var doc_title = document.getElementById("doc_title").title;
var likeDictionary = null;
var likeDictLen = 0;
const likeButtons = document.querySelectorAll(".likeContainer");
var like_type = 'unlike';
var liked_icon_w = "/static/images/like-fill-white.png";
var unliked_icon_w = "/static/images/like-outline-white.png"
var liked_icon = "/static/images/like-fill.png";
var unliked_icon = "/static/images/like-outline.png"
var message_collection = ["Add to your collection", "Added to your collection", "Currently in your collection", "Removed from your collection"];
var title = '';
var individual_index_pos = 0;

function likeToggle(index_value){
    toggle_boolean_var(index_value)
    if(likeButtons.length !=1){
        updateLikeView(index_value, true, true)
    }
    else{
        updateLikeView(index_value, true, false)
    }
    updateLikeStatus(likeDictionary[index_value])
}

function toggle_boolean_var(index_value){
    if(likeDictionary[index_value].isLiked){
        likeDictionary[index_value].isLiked = false;
    }
    else{
        likeDictionary[index_value].isLiked = true;
    }
}

function singleToggle(index_value){
    toggle_boolean_var(index_value)
}

function updateLikeView(index_value, is_initialized, is_multiple){
    if(is_multiple){
        caption = likeButtons[index_value].children[0]
        like_img = likeButtons[index_value].children[1]
    }
    else{
        caption = likeButtons[0].children[0]
        like_img = likeButtons[0].children[1]
    }

    if(likeDictionary[index_value].isLiked){
        if(is_initialized){
            if (message_collection.includes(caption.innerText)) {
                caption.innerText = 'Added to your collection'
            }
        }
        else{
            caption.innerText = 'Currently in your collection'
        }
        if(window.location.href.indexOf("audio") != -1){
            like_img.src = site_root + liked_icon_w
        }
        else{
            like_img.src = site_root + liked_icon
        }
    }
    else{
        if(is_initialized){
            if (message_collection.includes(caption.innerText)) {
                caption.innerText = 'Removed from your collection'
            }
        }
        else{
            caption.innerText = 'Add to your collection'
        }
        if(window.location.href.indexOf("audio") != -1){
            like_img.src = site_root + unliked_icon_w
        }
        else{
            like_img.src = site_root + unliked_icon
        }
    }
}

function loadLikes(){
    for(let i = 0; i < likeDictLen; i++){
        updateLikeView(i, false, true)
    }
}

function loadLikeSingle(song_id){
    for(let i = 0; i < likeDictLen; i++){
        if(song_id == likeDictionary[i].id){
            individual_index_pos = likeDictionary[i].position
            break;
        }
    }
    updateLikeView(individual_index_pos, false, false)
}

function getLikeStatus(){
    jQuery.ajax({ 
        url: "/api/likes/" + doc_title,
        type: 'GET', 
        timeout: 5000,
        success: function(data) { 
           if (data) {
            if(data == 'empty'){
                return
            }
             likeDictionary = data;
             if(likeDictionary[0].isLiked == 'logged_out'){
                 return
             }
             else{
                likeDictLen =  Object.keys(likeDictionary).length
                let no_num_in_url = isNaN(window.location.href.split(/\//)[5])
                if (no_num_in_url) {
                    // FOO NOTE: THIS NEEDS TO BE MODIFIED FOR THE DEPLOYED URL. IT CURRENTLY TAKES THE 3 FROM http://127.0.0.1:5000/audio/instrumental/3 CHANGE INDEX VALUE OF ARRAY
                    song_id = window.location.href.split(/\//)[5]
                    loadLikes()
                } 
                else {
                    song_id = window.location.href.split(/\//)[5]
                    loadLikeSingle(song_id)
                }
             }
           }
      }
    })   
}

function updateLikeStatus(obj){
    jQuery.ajax({ 
        url: "/api/likes/" + doc_title,
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

document.onload = getLikeStatus()