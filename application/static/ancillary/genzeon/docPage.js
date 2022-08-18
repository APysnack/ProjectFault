const modelLinkContainer = document.querySelector(".modelLinkContainer");
const hoverModal = document.querySelector('.hoverModal');
const clipBoard = document.querySelector('#clipBoard')
const closeBtn = document.querySelector("#closeBtn");
const submitCommentBtn = document.querySelector("#submitCommentBtn");
const addCommentField = document.querySelector("#addCommentField");

var modalOpen = false;

document.onkeydown = checkKey;

submitCommentBtn.addEventListener('click', (e)=>{
    if(addCommentField.value){
        let obj = {}
        obj.docParent = addCommentField.getAttribute('data-docParent')
        obj.comment = addCommentField.value
        addComment(obj)
    }
    else{
        alert("Please enter a comment")
    }
})

clipBoard.addEventListener('click', (e)=>{
    let link = clipBoard.getAttribute('data-docURL')
    copyToClipboard(link)
})

closeBtn.addEventListener('click', (e)=>{
    closeModal()
})

function copyToClipboard (text) {
    var dummy = document.createElement("textarea");
    document.body.appendChild(dummy);
    dummy.value = text;
    dummy.select();
    document.execCommand("copy");
    document.body.removeChild(dummy);
}

modelLinkContainer.addEventListener('click',(e)=>{
    if(modalOpen){
        closeModal()
    }
    else{
        openModal()
    }
})

function openModal(){
    hoverModal.style.display = 'flex'
    modalOpen = true;
}

function closeModal(){
    hoverModal.style.display = 'none'
    modalOpen = false;
}

function checkKey(e) {
    if(modalOpen){
        e = e || window.event;
        if (e.key == "Escape"){
        closeModal();
    }
  }
}

function addComment(comment){
    jQuery.ajax({ 
        url: "/api/add_doc_comment",
        type: 'POST', 
        contentType: 'application/json',
        data: JSON.stringify(comment),
        dataType: 'json',
        timeout: 5000,
        success: function(response) { 
             location.reload();
      }
   })
}

document.onload = closeModal()