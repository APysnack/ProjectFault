const toggleButton = document.querySelector(".toggleButton");
const site_root = window.location.origin
const header = document.getElementById('psHeader');
const navLinkContainer = document.querySelector(".navLinkContainer");
const navLink = document.getElementsByClassName("navLink");
const logoContainer = document.getElementById('logoContainer');

toggleButton.addEventListener('click', (e)=>{
    toggleDropDownMenu()
})


function toggleDropDownMenu(){
    header.classList.toggle('activeHeader');
    navLinkContainer.classList.toggle('activeNavLinkContainer');
    for (i = 0; i < navLink.length; i++) {
        navLink[i].classList.toggle('activeNavLink');
    }
    logoContainer.classList.toggle('activeLogoContainer');
}
