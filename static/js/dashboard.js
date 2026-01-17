// Toggle the visibility of the menu when clicked
function toggleHamburgerMenu() {
  const menu = document.getElementById("hamburgerMenu");
  
  // Toggle the show class
  menu.classList.toggle("show");
}

// Close the menu if clicking outside of it
document.addEventListener("click", function (event) {
  const menu = document.getElementById("hamburgerMenu");
  const button = document.querySelector(".hamburger-btn");

  // Close the menu if clicking outside of the button or the menu
  if (!menu.contains(event.target) && !button.contains(event.target)) {
    menu.classList.remove("show");  // Close the menu by removing the 'show' class
  }
});
