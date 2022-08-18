const sectionHeaders = document.querySelectorAll(".sectionHeader");
const lectureRows = document.querySelectorAll(".lectureRow");


function addListeners(){
    for (let i = 0; i < sectionHeaders.length; i++) {
        sectionHeaders[i].addEventListener('click', (e)=>{
            parent = sectionHeaders[i].parentNode;
            siblings = getAllSiblings(sectionHeaders[i], parent)
            for(let j =0; j < siblings.length; j++){
                siblings[j].classList.toggle('show');
            }
        });
    }

    for (let i = 0; i < lectureRows.length; i++) {
        lectureRows[i].addEventListener('click', (e)=>{
            sibling = lectureRows[i].nextElementSibling;
            sibling.classList.toggle('show');
        });
    }
}

function getAllSiblings(element, parent) {
    const children = [...parent.children];
    return children.filter(child => child !== element);
}

document.onload = addListeners();