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

// Tema
const themeToggle = document.getElementById("themeToggle");

// Carrega o tema salvo ao abrir a página
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "light") {
    document.documentElement.setAttribute("data-theme", "light");
    themeToggle.textContent = "☀️";
}

themeToggle.addEventListener("click", () => {
    const isLight = document.documentElement.getAttribute("data-theme") === "light";

    if (isLight) {
        document.documentElement.removeAttribute("data-theme");
        themeToggle.textContent = "🌙";
        localStorage.setItem("theme", "dark");
    } else {
        document.documentElement.setAttribute("data-theme", "light");
        themeToggle.textContent = "☀️";
        localStorage.setItem("theme", "light");
    }
});