const displayBtn = document.querySelector("#displayBookBtn");
const writingContainer = document.querySelectorAll(".writingContainer")[0];

var displayed = false;

displayBtn.addEventListener('click', (e)=>{
    toggleDisplay()
})

function toggleDisplay(){
    writingContainer.classList.toggle('show')
}