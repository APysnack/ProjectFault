createGameBtn = document.querySelector("#createGameBtn")
joinGameBtn = document.querySelector("#joinGameBtn")
createGameForm = document.querySelector("#createGameForm")
joinGameForm = document.querySelector("#joinGameForm")

var displayedForm = 'create'

document.onkeydown = checkKey;

function checkKey(e) {
    e = e || window.event;

    if (e.key == "ArrowLeft" || e.key == "ArrowRight") {
        updateFormDisplay()
      }
  }

document.querySelectorAll('.tabsArrow').forEach(tabsArrow => {
    tabsArrow.addEventListener('click', event => {
        updateFormDisplay()
    })
})


function updateFormDisplay(){
    if(displayedForm == 'create'){
        createGameForm.style.display = 'none';
        joinGameForm.style.display = 'flex';
        displayedForm = 'join'
    }
    else{
        createGameForm.style.display = 'flex';
        joinGameForm.style.display = 'none';
        displayedForm = 'create'
    }
}

createGameBtn.addEventListener('click', (e)=>{
    accessGame('create')
})

joinGameBtn.addEventListener('click', (e)=>{
    accessGame('join')
})


function accessGame(accessType){
    if(accessType == 'create'){
        roomName = document.querySelector("#cRoomNameInput").value
        roomPass = document.querySelector("#cRoomPwInput").value
        userName = document.querySelector("#cUserNameInput").value
    }
    else{
        roomName = document.querySelector("#jRoomNameInput").value
        roomPass = document.querySelector("#jRoomPwInput").value
        userName = document.querySelector("#jUserNameInput").value
    }

    if(roomName && roomPass && userName){
        var newGame = {}
        newGame.roomName = roomName
        newGame.roomPW = roomPass
        newGame.userName = userName
        newGame.accessType = accessType
        accessGameAPI(newGame)
    }
    
    else{
        alert('Please fill out all required fields')
    }
}

function accessGameAPI(newGame){
    jQuery.ajax({ 
         url: "/api/create-game/wt",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(newGame),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
              location.reload();
       }
    })
}