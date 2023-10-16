// values currently hardcoded. may implement an API call in the future to use the admin panel to create tabs more dynamically

var audioDetails = [
  "A collection of Alternative Instrumentals or Hip Hop beats that I've produced over the years using FL Studio",
  "Any form of music (Pop, Punk, Indie, etc.) that I've recorded which uses purely singing vocals",
  'Rap music with a more melodic emphasis and more of an influence from Indie/Pop/Rock genres',
  'Classic hip hop with little to no influence from Indie/Pop/Rock',
];
var audioLinks = [
  '/audio',
  '/audio/instrumental',
  '/audio/alternative',
  '/audio/indie-rap',
  '/audio/hip-hop',
];
var audioTitles = ['Instrumentals', 'Alternative', 'Indie Rap', 'Hip Hop'];
var audioTab = {
  id: 'audio',
  header: 'Audios',
  image: 'tab-photo-audio.jpg',
  details: audioDetails,
  titles: audioTitles,
  links: audioLinks,
};

var videoDetails = [
  'A free, comprehensive guide on how to write and record music, make your own graphics, promote your songs, and more!',
  'Video footage of me doing stand-up comedy',
  "Any music videos that I've appeared in or filmed/edited",
  'Live Hip Hop battling events where I oversaw the coordination, promotion, booking, & editing',
  "Live hip hop battles I've been involved in, where the emphasis is to implement play on words, often to insult your opponent in a witty or humorous way",
];
var videoLinks = [
  '/video',
  '/video/the-musicians-101',
  '/video/comedy-videos',
  '/video/music-videos',
  '/video/lrc-videos',
  '/video/video-battles',
];
var videoTitles = [
  "Musician's 101",
  'Stand Up Comedy',
  'Music Videos',
  'LRC Battles',
  'My Battles',
];
var videoTab = {
  id: 'video',
  header: 'Videos',
  image: 'tab-photo-video.jpg',
  details: videoDetails,
  titles: videoTitles,
  links: videoLinks,
};

var codeDetails = [
  'Details regarding my professional experience in software development',
  "Portfolio of personal projects I've developed. Excludes professional work.",
];
var codeLinks = ['/programming', '/resume', '/programming'];
var codeTitles = ['Resume', 'Software Projects'];
var codeTab = {
  id: 'code',
  header: 'Programming',
  image: 'tab-photo-code.jpg',
  details: codeDetails,
  titles: codeTitles,
  links: codeLinks,
};

var writingDetails = [
  'Books, blogs, jokes, and other writings',
  'Classic and modern poetry with less of a hip-hop influence',
  'Poetry written in the style of hip hop',
  "Written hip hop 'battles' where the emphasis is to implement play on words, often to insult your opponent in a witty or humorous way",
];
var writingLinks = [
  '/text',
  '/writings',
  '/poetry',
  '/topicals',
  '/text_battles',
];
var writingTitles = ['Writing', 'Poetry', 'Topicals', 'Battles'];
var writingTab = {
  id: 'writing',
  header: 'Writing',
  image: 'tab-photo-writing.jpg',
  details: writingDetails,
  titles: writingTitles,
  links: writingLinks,
};

var artDetails = [
  "Promotional flyers, website mock-ups, and other graphic designed I've created over the years using Adobe Photoshop",
  "Slightly artsy photographs that I've taken for fun",
];
var artLinks = ['/art', '/digital-art', '/photography'];
var artTitles = ['Digital Art', 'Photography'];
var artTab = {
  id: 'art',
  header: 'Digital Art',
  image: 'tab-photo-art.jpg',
  details: artDetails,
  titles: artTitles,
  links: artLinks,
};

var miscDetails = [
  'Have any questions, comments, concerns? Reach out to me via this form and I will respond as soon as possible',
  'More details about me',
  'All future projects are facilitated with donations from viewers like you. Please consider donating any amount, every dollar helps!',
  'Terms and conditions providing rules and guidelines for anyone who wishes to use this website and/or any of the free content provided',
  'Details regarding how this website collects, handles, and processes data from visitors.',
];
var miscLinks = [
  '/media',
  '/contact',
  '/about',
  '/donate',
  '/terms',
  '/privacy',
];
var miscTitles = ['About Me', 'Terms', 'Privacy'];
var miscTab = {
  id: 'misc',
  header: 'Miscellaneous',
  image: 'tab-photo-misc.jpg',
  details: miscDetails,
  titles: miscTitles,
  links: miscLinks,
};

tabList = [codeTab, audioTab, videoTab, writingTab, artTab, miscTab];

var activeHeader = document.getElementById('activeHeader');
var additionalInfo = document.getElementById('tabAdditionalInfo');
var activeImg = document.getElementById('activeImage');
var activeLinkHeader = document.getElementById('contentHeader');
var linksContainer = document.getElementById('tabLinksContainer');
var leftArrow = document.getElementById('leftArrow');
var rightArrow = document.getElementById('rightArrow');

var activeIndex = 0;

document.onkeydown = checkKey;

leftArrow.addEventListener('click', (e) => {
  shiftTabLeft();
});

rightArrow.addEventListener('click', (e) => {
  shiftTabRight();
});

document.querySelectorAll('.tabSection').forEach((item) => {
  item.addEventListener('click', (event) => {
    swapButtonIndex(item);
  });
});

function swapActiveBody(index) {
  activeIndex = index;
  activeHeader.innerText = tabList[index].header.toUpperCase();
  path = 'url("' + site_root + '/static/images/' + tabList[index].image + '")';
  activeImg.style.backgroundImage = path;

  activeLinkHeader.innerText = 'Navigate ' + tabList[index].header;
  activeLinkHeader.href = site_root + tabList[index].links[0];
  removeAllChildNodes(linksContainer);
  removeAllChildNodes(additionalInfo);
  for (let j = 0; j < tabList[index].titles.length; j++) {
    let thisLink = document.createElement('a');
    thisLink.href = site_root + tabList[index].links[j + 1];
    thisLink.classList.add('contentLink');
    let newDiv = document.createElement('div');
    newDiv.classList.add('contentLinkText');
    newDiv.innerText = tabList[index].titles[j];
    thisLink.append(newDiv);
    linksContainer.append(thisLink);
  }
  for (let k = 0; k < tabList[index].titles.length; k++) {
    let newDiv = document.createElement('div');
    newDiv.classList.add('detailsBlock');

    let blockHead = document.createElement('a');
    blockHead.classList.add('detailsBlockHead');
    blockHead.innerText = tabList[index].titles[k].toUpperCase();
    blockHead.href = site_root + tabList[index].links[k + 1];

    let blockText = document.createElement('div');
    blockText.classList.add('detailsBlockText');
    blockText.innerText = tabList[index].details[k];

    newDiv.append(blockHead);
    newDiv.append(blockText);

    additionalInfo.append(newDiv);
  }
}

function swapButtonIndex(e) {
  let calling_tab = e.dataset.tab;
  for (let i = 0; i < tabList.length; i++) {
    if (calling_tab == tabList[i].id) {
      swapActiveBody(i);
      break;
    }
  }
}

function shiftTabLeft() {
  let new_index = activeIndex - 1;
  if (new_index < 0) {
    new_index = tabList.length - 1;
  }
  swapActiveBody(new_index);
}

function shiftTabRight() {
  let new_index = activeIndex + 1;
  if (new_index >= tabList.length) {
    new_index = 0;
  }
  swapActiveBody(new_index);
}

function removeAllChildNodes(parent) {
  if (parent.id == 'tabAdditionalInfo') {
    while (parent.lastChild) {
      parent.removeChild(parent.lastChild);
    }
  } else {
    while (parent.lastChild.id !== 'contentHeader') {
      parent.removeChild(parent.lastChild);
    }
  }
}

function checkKey(e) {
  e = e || window.event;

  if (e.key == 'ArrowLeft') {
    shiftTabLeft();
  } else if (e.key == 'ArrowRight') {
    shiftTabRight();
  }
}

document.onload = swapActiveBody(0);
