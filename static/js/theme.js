document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const savedTheme = localStorage.getItem("theme");

    function applyTheme(theme) {
        const isLight = theme === "light";

        if (isLight) {
            document.documentElement.setAttribute("data-theme", "light");
            localStorage.setItem("theme", "light");
        } else {
            document.documentElement.setAttribute("data-theme", "dark");
            localStorage.setItem("theme", "dark");
        }

        if (themeToggle) {
            themeToggle.classList.toggle("is-light", isLight);
            themeToggle.setAttribute(
                "aria-label",
                isLight ? "Mudar para tema escuro" : "Mudar para tema claro"
            );
        }
    }

    applyTheme(savedTheme === "light" ? "light" : "dark");

    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const isLight = document.documentElement.getAttribute("data-theme") === "light";
            applyTheme(isLight ? "dark" : "light");
        });
    }
});