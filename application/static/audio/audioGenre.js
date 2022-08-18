document.querySelectorAll('.imageBackground').forEach(item => {
    item.addEventListener('click', event => {
      route_to_song(item)
    })
})

function route_to_song(e){
    genre = e.dataset.genre
    song = e.dataset.song
    new_url = site_root + '/audio/' + genre + '/' + song
    window.location.href = new_url
}