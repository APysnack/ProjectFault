rowContainers = document.querySelectorAll('.songRowContainer')
accountAudio = document.querySelectorAll('.accountPgAudio')
accountForum = document.querySelectorAll('.accountForumPosts')[0]
accountText = document.querySelectorAll('.accountPgText')[0]
accountVideo = document.querySelectorAll('.accountPgVideo')[0]
accountImages = document.querySelectorAll('.accountPgImages')[0]
accountEdit = document.querySelectorAll('.accountPgEdit')[0]
accountContent = document.getElementById('accountPageContent')

var lastActiveIndex = -1;
var currentAccountPage = ''

function toggle_active(e){
    let thisIndex = parseInt(e.title)
    if(thisIndex != lastActiveIndex){
        e.style.backgroundColor = '#df2500';
        if(lastActiveIndex != -1){
            rowContainers[lastActiveIndex].style.backgroundColor = '#2e3a46';
        }
        lastActiveIndex = thisIndex;
        togglePlayButton('forcePlayDisplay')
    }
}


document.querySelectorAll('.accountNavLink').forEach(item => {
    item.addEventListener('click', event => {
        navPage = item.getAttribute('data-navPage')
        populate(navPage)
    })
})


function accountPgInit(){
    populate('forum')
}

function populate(navPage){
    console.log(navPage)
    console.log(accountForum)
    closeOpenAccountPage()
    openAccountPage(navPage)
}

function openAccountPage(navPage){
    if(navPage == 'audio'){
        for(let i = 0; i < accountAudio.length; i++){
            accountAudio[i].classList.toggle('showAccountPage')
        }
        currentAccountPage = 'audio'
    }
    else if(navPage == 'video'){
        accountVideo.classList.toggle('showAccountPage')
        currentAccountPage = 'video'
    }
    else if(navPage == 'forum'){
        accountForum.classList.toggle('showAccountPage')
        currentAccountPage = 'forum'
    }
    else if(navPage == 'images'){
        accountImages.classList.toggle('showAccountPage')
        currentAccountPage = 'images'
    }
    else if(navPage == 'text'){
        accountText.classList.toggle('showAccountPage')
        currentAccountPage = 'text'
    }
    else{
        accountEdit.classList.toggle('showAccountPage')
        currentAccountPage = 'edit'
    }
}

function closeOpenAccountPage(){
    if(currentAccountPage == ''){}
    else if(currentAccountPage == 'audio'){
        for(let i = 0; i < accountAudio.length; i++){
            accountAudio[i].classList.toggle('showAccountPage')
        }
    }
    else if(currentAccountPage == 'video'){
        accountVideo.classList.toggle('showAccountPage')
    }
    else if(currentAccountPage == 'forum'){
        console.log("here")
        accountForum.classList.toggle('showAccountPage')
    }
    else if(currentAccountPage == 'images'){
        accountImages.classList.toggle('showAccountPage')
    }
    else if(currentAccountPage == 'text'){
        accountText.classList.toggle('showAccountPage')
    }
    else{
        accountEdit.classList.toggle('showAccountPage')
    }
}

document.onload = accountPgInit()