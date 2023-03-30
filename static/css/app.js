const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const header = document.querySelector(".head");

hamburger.addEventListener("click", ()=>{
  //add active class
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
  header.classList.toggle("bg");
})

document.querySelectorAll(".nav-link").forEach(element => element.addEventListener("click",()=>{
  hamburger.classList.remove("active");
  navMenu.classList.remove("active");
  header.classList.remove("bg");
}));

