document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("toggleWhats");
    const btnsWhatsapp = document.querySelectorAll(".btn-whatsapp");

    if (!toggle) return; // evita erro se não existir

    let ativo = localStorage.getItem("whatsAuto") === "true";

    aplicarEstado();

    toggle.addEventListener("click", () => {
        ativo = !ativo;
        localStorage.setItem("whatsAuto", ativo);
        aplicarEstado();
    });

    function aplicarEstado() {

        // botão verde
        if (ativo) {
            toggle.classList.add("active");
        } else {
            toggle.classList.remove("active");
        }

        // esconder/mostrar botões WhatsApp
        btnsWhatsapp.forEach(btn => {
            btn.style.display = ativo ? "none" : "inline-block";
        });
    }
});