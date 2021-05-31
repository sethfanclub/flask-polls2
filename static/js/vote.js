const btnVote = document.getElementById('btn-vote')
const radioBtns = document.querySelectorAll(".vote-form > div > input[type='radio']")

btnVote.addEventListener('click', function() {
  onVote()
})

function onVote() {
  for (let btn of radioBtns) {
    btn.classList.add('hide')
  }
}