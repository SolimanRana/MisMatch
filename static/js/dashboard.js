function toggleHamburgerMenu() {
  const menu = document.getElementById("hamburgerMenu");
  menu.classList.toggle("show");  // Toggle visibility on click
}

document.addEventListener("click", function (event) {
  const menu = document.getElementById("hamburgerMenu");
  const button = document.querySelector(".hamburger-btn");

  if (!menu.contains(event.target) && !button.contains(event.target)) {
    menu.classList.remove("show");  // Close the menu if clicked outside
  }
});
