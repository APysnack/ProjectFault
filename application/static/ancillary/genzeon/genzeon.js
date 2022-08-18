const sbmBtn = document.querySelector(".sbmBtn");
const imageInput = document.querySelector("#myFile");
const addModelBtn = document.querySelector("#addModelBtn");
const nameInput = document.querySelector(".nameInput");
const modelForm = document.querySelector("#newMdlForm");
const modelModal = document.querySelector(".modelModal");
const tinListContainer = document.querySelector("#tinListContainer");
const tinModelAddBtn = document.querySelector("#tinModelAddBtn");
const tinSelector = document.querySelector("#tinSelector");
const closeBtn = document.querySelector("#closeBtn");

var imgFile = null;
var newModel = {};
var extension = null;
var modalOpen = false;
var model_type = null;

document.onkeydown = checkKey;

closeBtn.addEventListener('click', (e)=>{
    closeModal()
})

tinModelAddBtn.addEventListener('click', (e)=>{
    let modelObj = {}
    modelObj.modelNum = model_type
    modelObj.tinNum = tinSelector.value
    var node = document.createElement("LI");
    var textnode = document.createTextNode(tinSelector.value);
    node.appendChild(textnode)
    tinListContainer.appendChild(node)
    tinToModel(modelObj)
})

function checkKey(e) {
    if(modalOpen){
        e = e || window.event;
        if (e.key == "Escape"){
        closeModal();
    }
  }
}

function openModel(model_type){
    modalOpen = true;
    modelModal.style.display = "block"
    generateTINList(model_type)
}

function closeModal(){
    modalOpen = false;
    modelModal.style.display = "none"
    model_type = null;
}

addModelBtn.addEventListener('click', (e)=>{
    modelForm.classList.toggle('showForm')
});

document.querySelectorAll('.genzModel').forEach(model => {
    model.addEventListener('click', event => {
        if(model_type == null){
            model_type = model.getAttribute('data-modelType')
        }
        if(modalOpen){
            closeModal()
        }
        else{
            openModel(model_type)
        }
    })
})

function generateTINList(model_type){
    getTINs(model_type)
}

function populateModal(data){
    removeAllChildNodes(tinListContainer)
    for(let i =0; i < data.length; i++){
        var node = document.createElement("LI");
        var textnode = document.createTextNode(data[i]);
        node.appendChild(textnode)
        tinListContainer.appendChild(node)
    }
}

function removeAllChildNodes(parent) {
    while (parent.lastChild) {
            parent.removeChild(parent.lastChild);
    }
}

document.querySelectorAll('.deleteBtn').forEach(deleteBtn => {
    deleteBtn.addEventListener('click', event => {
        let modelName = deleteBtn.getAttribute('data-modelName')
        let myObj = { "modelName":modelName};
        removeObject(myObj)
    })
})



sbmBtn.addEventListener('click', (e)=>{
    if(imgFile){
        fileName = nameInput.value;
        if(imgFile.name.includes(".jpg")){
            extension = '.jpg'
        }
        if(imgFile.name.includes(".png")){
            extension = '.png'
        }
        getBase64(imgFile).then(data => storeJSON(data, fileName, extension));
    }
})

function storeJSON(data, fileName, ext){
    newModel.name = fileName;
    newModel.img = data;
    newModel.ext = ext;
    callAjax(newModel)
}

function getBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        let encoded = reader.result.toString().replace(/^data:(.*,)?/, '');
        if ((encoded.length % 4) > 0) {
          encoded += '='.repeat(4 - (encoded.length % 4));
        }
        resolve(encoded);
      };
      reader.onerror = error => reject(error);
    });
}

window.addEventListener("paste", (e)=>{
    if(e.clipboardData.files.length > 0){
        const fileInput = document.querySelector("#myFile");
        fileInput.files = e.clipboardData.files;
        if(e.clipboardData.files[0].type.startsWith("image/")){
            imgFile = e.clipboardData.files[0];
            setPreviewImage(imgFile)
        }
    }
})

function setPreviewImage(file){
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = () => {
        document.querySelector("#imagePreview").src = fileReader.result;
    };
}

imageInput.onchange = evt => {
    [temp] = imageInput.files
    imgFile = temp
    if (imgFile) {
      setPreviewImage(imgFile)
    }
}

function callAjax(modelDict){
    jQuery.ajax({ 
         url: "/api/add_tin_model",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(modelDict),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
              location.reload();
       }
    })
}

function tinToModel(modelObj){
    jQuery.ajax({ 
         url: "/api/add_tin_to_model",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(modelObj),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
              
       }
    })
}

function removeObject(obj){
    jQuery.ajax({ 
        url: "/api/del_tin_model",
        type: 'POST', 
        contentType: 'application/json',
        data: JSON.stringify(obj),
        dataType: 'json',
        timeout: 5000,
        success: function(response) { 
          location.reload();
        }
      })
}

function getTINs(modelName){
    jQuery.ajax({ 
         url: "/api/get-model-tins/" + modelName,
         type: 'GET', 
         timeout: 5000,
         success: function(data) { 
            if (data) {
              populateModal(data)
            }
       }
    })
}