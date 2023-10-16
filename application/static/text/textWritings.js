const displayBtn = document.querySelector('#displayBookBtn');
const writingContainer = document.querySelectorAll('.writingContainer')[0];
const googleDoc = document.querySelector('#googleDoc');
let displayed = false;

window.onload = function () {
  updateGoogle();
};

displayBtn.addEventListener('click', () => {
  toggleDisplay();
});

function toggleDisplay() {
  writingContainer.classList.toggle('show');
}

function updateGoogle() {
  googleDoc.src =
    'https://docs.google.com/document/d/e/2PACX-1vQJ1k3JHZC5VfoRNzXyNtQujjdKt4uDlkKh0en4yc2LwCp8fc3p9zauV7du-3Hj36XkDlDp9ClvJrGD/pub?embedded=true';
}
