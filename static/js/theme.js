// static/js/theme.js

document.addEventListener("DOMContentLoaded", () => {

    const themeToggle =
        document.getElementById("themeToggle");

    // PEGA TEMA SALVO
    const savedTheme =
        localStorage.getItem("theme");

    // APLICA TEMA
    if (savedTheme === "light") {

        document.documentElement
            .setAttribute("data-theme", "light");

        if (themeToggle) {

            themeToggle.textContent = "☀️";

        }

    } else {

        document.documentElement
            .removeAttribute("data-theme");

        if (themeToggle) {

            themeToggle.textContent = "🌙";

        }

    }

    // BOTÃO TROCAR TEMA
    if (themeToggle) {

        themeToggle.addEventListener("click", () => {

            const isLight =
                document.documentElement
                .getAttribute("data-theme") === "light";

            if (isLight) {

                document.documentElement
                    .removeAttribute("data-theme");

                localStorage.setItem("theme", "dark");

                themeToggle.textContent = "🌙";

            } else {

                document.documentElement
                    .setAttribute("data-theme", "light");

                localStorage.setItem("theme", "light");

                themeToggle.textContent = "☀️";

            }

        });

    }

});