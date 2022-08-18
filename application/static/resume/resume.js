var run = setInterval(loadFrame, 15);
const loadCircles = document.querySelectorAll(".loadCircle");
const loadNumbers = document.querySelectorAll(".loadNumber");
var counter = 0;
var counterList = [85, 75, 80, 80, 85, 85, 90, 90, 85, 90];
var counterMax = 90;

var tags = document.getElementsByClassName("tag");

function addListeners(){
    for (var i = 0; i < tags.length; i++) {
        tags[i].addEventListener('click', (e)=>{
            e.target.classList.toggle('remove');
            e.preventDefault();
        })
    }   
}

function loadFrame() {
    let i = 0;
    counter = counter + 1;
    loadCircles.forEach((circle)=>{
        circle.style.strokeDashoffset = (400 - (400*(counterList[i]/100)) + counter);
        i = i + 1;
    });

    i = 0;
    loadNumbers.forEach((num)=>{
        if(counter < counterList[i]){
            num.textContent = (counter+1) + " / 100";
        }
        i = i + 1;
    });

    if(counter == (counterMax + 1)){
        clearInterval(run);
    }
}

document.onload = addListeners();