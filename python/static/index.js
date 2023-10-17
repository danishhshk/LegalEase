// ;(function () {
var btnLogin = document.querySelector('.user-btn')
// btnLogin.addEventListener('click', ShowModel)
function ShowModel() {
  document.querySelector('.signIn').classList.add('ShowSignIn')
  document.querySelector('.nav').classList.add('blur')
  document.querySelector('.main-cont').classList.add('blur')
}
document.querySelector('.cancel-btn').addEventListener('click', () => {
  document.querySelector('.signIn').classList.remove('ShowSignIn')
  document.querySelector('.nav').classList.remove('blur')
  document.querySelector('.main-cont').classList.remove('blur')
})

// })
