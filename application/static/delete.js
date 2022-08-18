document.querySelectorAll('.deleteButton').forEach(deleteBtn => {
    deleteBtn.addEventListener('click', event => {
        let type = deleteBtn.getAttribute('data-dbType')
        let id = deleteBtn.getAttribute('data-dbObject')
        deleteObject(type, id)
    })
})

function deleteObject(type, id){
    myObj = { "type":type, "id":id };
    removeDBObject(myObj)
}

function removeDBObject(obj){
    jQuery.ajax({ 
        url: "/api/delete",
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