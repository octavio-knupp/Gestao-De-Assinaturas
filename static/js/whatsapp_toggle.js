console.log("JS WHATSAPP CARREGADO");

document.addEventListener("DOMContentLoaded", async () => {

    const toggle = document.getElementById("toggleWhats");

    const btnsWhatsapp = document.querySelectorAll(
        ".btn-whatsapp"
    );

    if (!toggle) return;

    let ativo = false;

    // =========================
    // CARREGAR ESTADO DO DJANGO
    // =========================

    try {

        const response = await fetch(
            "/whatsapp/get-whatsapp-automation-status/"
        );

        const data = await response.json();

        ativo = data.active;

        aplicarEstado();

    } catch (error) {

        console.error(
            "Erro ao carregar status:",
            error
        );
    }

    // =========================
    // CLICK TOGGLE
    // =========================

    toggle.addEventListener("click", async () => {

        ativo = !ativo;

        aplicarEstado();

        try {

            const response = await fetch(
                "/whatsapp/toggle-whatsapp-automation/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie(
                            "csrftoken"
                        ),
                    },

                    body: JSON.stringify({
                        active: ativo
                    })
                }
            );

            const data = await response.json();

            console.log(data);

        } catch (error) {

            console.error(
                "Erro toggle WhatsApp:",
                error
            );
        }
    });

    // =========================
    // UI
    // =========================

    function aplicarEstado() {

        if (ativo) {

            toggle.classList.add("active");

        } else {

            toggle.classList.remove("active");
        }

        btnsWhatsapp.forEach(btn => {

            btn.style.display = ativo
                ? "none"
                : "inline-block";
        });
    }

    // =========================
    // CSRF
    // =========================

    function getCookie(name) {

        let cookieValue = null;

        if (document.cookie && document.cookie !== "") {

            const cookies = document.cookie.split(";");

            for (let i = 0; i < cookies.length; i++) {

                const cookie = cookies[i].trim();

                if (
                    cookie.substring(0, name.length + 1)
                    === (name + "=")
                ) {

                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );

                    break;
                }
            }
        }

        return cookieValue;
    }
});