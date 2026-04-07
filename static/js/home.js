const sidebar = document.getElementById("sidebar");
const menuBtn = document.getElementById("menuBtn");
const perfilBtn = document.getElementById("perfilBtn");
const perfilSubmenu = document.getElementById("perfilSubmenu");

menuBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
});

perfilBtn.addEventListener("click", () => {

    perfilSubmenu.classList.toggle("active");

});