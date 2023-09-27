var page_title = document.getElementById('page_title').title;
const audioPlayerContainer = document.querySelector('#audioPlayerContainer');
const audioPlayer = document.querySelector('#audioPlayer');
const controlsContainer = document.querySelector('#controlsContainer');
const songTitle = document.querySelector('#songTitle');
const buttonContainer = document.querySelector('#buttonContainer');
const audioImage = document.querySelector('#audioPlayerThumb');
const prevAudioBtn = document.querySelector('#prevAudioBtn');
const nextAudioBtn = document.querySelector('#nextAudioBtn');
const cur_song = document.querySelector('#current_song');
const progress = document.querySelector('#progressBar');
const progressContainer = document.querySelector('#progressContainer');
var audioDictionary = null;
var audioDictLen = 0;
var isPlaying = false;
var nowPlaying = 0;
var clickCount = 0;
var timeout = 300;
var lastIndex = 0;

if (cur_song != null) {
  cur_song.addEventListener('timeupdate', updateProgress);
  cur_song.addEventListener('ended', playNext);
  progressContainer.addEventListener('click', setProgress);
  document.querySelectorAll('.songPlayBtn').forEach((item) => {
    item.addEventListener('click', (event) => {
      event.stopPropagation();
      let position = item.dataset.song_position;
      playTrack(position);
    });
  });

  document.querySelectorAll('.playPause').forEach((item) => {
    item.addEventListener('click', (event) => {
      play_pause();
    });
  });

  prevAudioBtn.addEventListener('click', (e) => {
    clicks('prev');
  });

  nextAudioBtn.addEventListener('click', (e) => {
    clicks('next');
  });

  document.ondblclick = function (evt) {
    if (window.getSelection) window.getSelection().removeAllRanges();
    else if (document.selection) document.selection.empty();
  };
}

function updateProgress(e) {
  const { duration, currentTime } = e.srcElement;
  const progressPercent = (currentTime / duration) * 100;
  progress.style.width = `${progressPercent}%`;
}

function setProgress(e) {
  const width = this.clientWidth;
  const clickX = e.offsetX;
  const duration = cur_song.duration;
  cur_song.currentTime = (clickX / width) * duration;
}

function clicks(caller) {
  clickCount++;
  if (clickCount == 1) {
    setTimeout(function () {
      if (clickCount == 1) {
        if (caller == 'prev') {
          startOver();
        } else {
          playNext();
        }
      } else {
        if (caller == 'prev') {
          playPrev();
        } else {
          playNext();
        }
      }
      clickCount = 0;
    }, timeout || 300);
  }
}

function playPrev() {
  let new_index = nowPlaying - 1;
  if (new_index < 0) {
    new_index = audioDictLen - 1;
  }

  togglePlayButton('forcePlayDisplay');
  loadSong(new_index);
  cur_song.play();
  isPlaying = true;
}

function playNext() {
  let new_index = nowPlaying + 1;

  if (new_index >= audioDictLen) {
    new_index = 0;
  }

  togglePlayButton('forcePlayDisplay');
  loadSong(new_index);
  cur_song.play();
  isPlaying = true;
}

function startOver() {
  cur_song.currentTime = 0;
  cur_song.play();
  isPlaying = true;
}

function playTrack(index) {
  if (lastIndex != index) {
    loadSong(index);
    cur_song.play();
    isPlaying = true;
    lastIndex = index;
    togglePlayButton('forcePlayDisplay');
  } else {
    play_pause();
  }
}

function init() {
  getData();
}

function play_pause() {
  if (isPlaying) {
    pauseSong();
  } else {
    playSong();
  }
}

function loadSong(index) {
  nowPlaying = parseInt(index);

  audioImage.src = audioDictionary[index].image_file;
  songTitle.innerText = audioDictionary[index].title;
  songPath = audioDictionary[index].url;
  cur_song.src = songPath;
}

function togglePlayButton(param) {
  if (param == 'forcePlayDisplay') {
    playAudioBtn.style.display = 'flex';
    pauseAudioBtn.style.display = 'none';
  }

  if (playAudioBtn.style.display == 'none') {
    playAudioBtn.style.display = 'flex';
    pauseAudioBtn.style.display = 'none';
  } else {
    playAudioBtn.style.display = 'none';
    pauseAudioBtn.style.display = 'flex';
  }
}

function playSong() {
  console.log(cur_song);
  togglePlayButton();
  cur_song.play();
  isPlaying = true;
}

function pauseSong() {
  togglePlayButton();
  cur_song.pause();
  isPlaying = false;
}

function getData() {
  jQuery.ajax({
    url: '/api/likes/' + page_title,
    type: 'GET',
    timeout: 5000,
    success: function (data) {
      if (data) {
        if (data == 'empty') {
          return;
        }
        audioDictionary = data;
        audioDictLen = Object.keys(audioDictionary).length;
        let no_num_in_url = isNaN(window.location.href.split(/\//)[5]);
        if (no_num_in_url) {
          first_index = 0;
        } else {
          song_id = window.location.href.split(/\//)[5];
          for (let i = 0; i < audioDictLen; i++) {
            if (song_id == audioDictionary[i].id) {
              first_index = audioDictionary[i].position;
              break;
            }
          }
        }
        loadSong(first_index);
      }
    },
  });
}

document.onload = init();
