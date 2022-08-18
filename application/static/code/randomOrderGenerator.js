var onlyOneDetails = "The \"Only One\" algorithm will randomly select one item from your list. This can be used to determine a \"first player\" for a game, or to simulate a single \"winner\" from a draw. You can enter as many or as few items as you wish"
var randomizerDetails = "The \"Randomize All\" algorithm will take all of the items in your list and shuffle the order randomly. You can enter as many or as few items as you wish and repeat this process as many times as you'd like"
var seederDetails = "**This function is still being developed** The \"Tournament Seeder\" algorithm will take all of the items in your list and generate a tournament-style bracket with randomized seeding"

var textDetails = {"onlyOne":onlyOneDetails, "randomizer":randomizerDetails, "seeder":seederDetails}

var newEntry = document.getElementById("newName");
const submissionBtn = document.getElementById("newNameSubmit");
const entryList = document.getElementById("entryList");
const generator = document.getElementById("generator");
const textBox = document.getElementById("typeDescriptionContainer");
const generateBtn = document.getElementById("generateResultsBtn");
const closeModal = document.getElementById("closeModal");
var winnerVar = document.getElementById("winnerVar");
var numItemsVar = document.getElementById("numItemsVar");
var winnerName = document.getElementById("winnerName");
var resultsModal = document.getElementById("resultsModal")
var modalHeader = document.getElementById("modalHeader")

var orderedArray = []
var currentGenerator = 'onlyOne';
var modalOpen = false;

document.onkeydown = checkKey;

submissionBtn.addEventListener('click', (e)=>{
    let newName = newEntry.value
    if(newName){
        addName(newName)
    }
    else{
        alert("please enter a value")
    }
})

function addName(newName){
    orderedArray.push(newName)
    removeAllChildNodes(entryList)
    populateList(orderedArray)
    newEntry.value = ""
}

function removeName(position){
    orderedArray.splice(position, 1)
    removeAllChildNodes(entryList)
    populateList(orderedArray)
}

function getRandomInt() {
    return Math.floor(Math.random() * orderedArray.length);
}

function populateList(localArray){
    if(localArray.length > 0){
        for(let i = 0; i < localArray.length; i++){
            entryRow = document.createElement("div");
            entryRow.classList.add("entryRow")

            entryNum = document.createElement("span")
            entryNum.classList.add("entryNum")
            entryNum.appendChild(document.createTextNode(i));

            
            entry = document.createElement("LI");
            entry.appendChild(document.createTextNode(localArray[i]));

            deleteEntryBtn = document.createElement("button")
            deleteEntryBtn.classList.add("deleteEntryBtn")
            deleteEntryBtn.setAttribute('data-arrayPosition', i)
            deleteEntryBtn.appendChild(document.createTextNode("delete"));

            entryRow.append(entryNum)
            entryRow.append(entry)
            entryRow.append(deleteEntryBtn)

            entryList.append(entryRow)
        }
    }
}

newName.onkeypress = function(e){
    if (!e) e = window.event;
    var keyCode = e.code || e.key;
    if (keyCode == 'Enter'){
        e.preventDefault();
        let newName = e.target.value
        addName(newName)
    }
  }

function updateTextBox(){
    textBox.innerText = textDetails[currentGenerator]
}

function removeAllChildNodes(parent) {
    while (parent.lastChild) {
            parent.removeChild(parent.lastChild);
    }
}

function generateOne(){
    modalHeader.innerText = "\"Only One\" Generator"
    let winningIndex = getRandomInt()
    let winner = orderedArray[winningIndex]
    winnerName.innerText = winner.toUpperCase() + '!'
    winnerVar.innerText = winner
    numItemsVar.innerText = orderedArray.length
    resultsModal.style.display = 'flex'
    modalOpen = true;
}

function randomizeAll(){
    let oldArray = orderedArray
    orderedArray = shuffle(oldArray)
    removeAllChildNodes(entryList)
    populateList(orderedArray)
}

function shuffle(array) {
    var currentIndex = array.length,  randomIndex;
  
    while (0 !== currentIndex) {
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex--;
      [array[currentIndex], array[randomIndex]] = [
        array[randomIndex], array[currentIndex]];
    }
  
    return array;
  }

function seedBracket(){
    alert("This function is currently still being developed. Please try one of the other generators")
    return
}

function closeModalWindow(){
    resultsModal.style.display = 'none';
    modalOpen = false;
}

function checkKey(e) {
    if(modalOpen){
        e = e || window.event;
        if (e.key == "Escape"){
            closeModalWindow();
        }
    }
}

generator.addEventListener('change', (e)=>{
    currentGenerator = e.target.value
    updateTextBox()
});

document.addEventListener('click',function(e){
    if(e.target.classList == 'deleteEntryBtn'){
        let position = e.target.getAttribute('data-arrayPosition')
        removeName(position)
    }
});

generateBtn.addEventListener('click', (e)=>{
    if(orderedArray.length < 1){
        alert("You must add at least one item to the list")
    }
    else if(currentGenerator == 'onlyOne'){
        generateOne()
    }
    else if(currentGenerator == 'randomizer'){
        randomizeAll()
    }
    else{
        seedBracket()
    }
})

closeModal.addEventListener('click', (e)=>{
    closeModalWindow()
})

document.onload = updateTextBox()