const upArrow = document.querySelectorAll(".up-arrow");
const downArrow = document.querySelectorAll(".down-arrow");
const votes = document.querySelectorAll(".numVotes");
const submit = document.querySelector(".sbm");
var countDict = []

function addListeners(){
    for (let i = 0; i < upArrow.length; i++) {
        let project_id = upArrow[i].parentNode.firstElementChild.innerText

        up_style = window.getComputedStyle(upArrow[i])
        down_style = window.getComputedStyle(downArrow[i])

        if (down_style.getPropertyValue('fill') != 'rgb(206, 212, 218)'){
            countDict.push({
                key:   project_id,
                value: -1
            });
        }
        else if (up_style.getPropertyValue('fill') != 'rgb(206, 212, 218)'){
            countDict.push({
                key:   project_id,
                value: 1
            });
        }
        else{
            countDict.push({
                key:   project_id,
                value: 0
            });
        }

        upArrow[i].addEventListener('click', (e)=>{
            up_style = window.getComputedStyle(upArrow[i])
            down_style = window.getComputedStyle(downArrow[i])

            if (down_style.getPropertyValue('fill') != 'rgb(206, 212, 218)'){
            }
            else if (up_style.getPropertyValue('fill') == 'rgb(206, 212, 218)'){
                countDict[i].value = 1;
                upArrow[i].style.fill = '#00df9a'
                var newNum = parseInt(votes[i].innerText) + 1
                votes[i].innerText = newNum + " Votes"
            }
            else{
                countDict[i].value = 0;
                upArrow[i].style.fill = '#ced4da'
                var newNum = parseInt(votes[i].innerText) - 1
                votes[i].innerText = newNum + " Votes"
            }
        });

        downArrow[i].addEventListener('click', (e)=>{
            up_style = window.getComputedStyle(upArrow[i])
            down_style = window.getComputedStyle(downArrow[i])

            if (up_style.getPropertyValue('fill') != 'rgb(206, 212, 218)'){
            }
            else if (down_style.getPropertyValue('fill') == 'rgb(206, 212, 218)'){
                countDict[i].value = -1;
                downArrow[i].style.fill = '#df2500'
                var newNum = parseInt(votes[i].innerText) - 1
                votes[i].innerText = newNum + " Votes"
            }
            else{
                countDict[i].value = 0;
                downArrow[i].style.fill = '#ced4da'
                var newNum = parseInt(votes[i].innerText) + 1
                votes[i].innerText = newNum + " Votes"
            }
        });
    }
}

submit.addEventListener('click', (e)=>{
    if(submit.id == "logged_out"){
        alert("You must be logged in to use this feature")
    }
    else{
        callAjax(countDict)
    }
})

function callAjax(countDict){
    jQuery.ajax({ 
         url: "/upcoming",
         type: 'POST', 
         contentType: 'application/json',
         data: JSON.stringify(countDict),
         dataType: 'json',
         timeout: 5000,
         success: function(response) { 
            if (response.redirect) {
                window.location.href = response.redirect;
            }
       }
    })
}

document.onload = addListeners();