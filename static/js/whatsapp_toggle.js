document.addEventListener('DOMContentLoaded', () => {

    const toggle = document.getElementById('toggleWhats');

    // Estado padrão: DESLIGADO
    let ativo = false;

    // Carrega do localStorage
    if (localStorage.getItem('whatsAtivo') !== null) {
        ativo = localStorage.getItem('whatsAtivo') === 'true';
    }

    // Atualiza checkbox
    if (toggle) {
        toggle.checked = ativo;

        toggle.addEventListener('change', () => {
            localStorage.setItem('whatsAtivo', toggle.checked);
        });
    }

    // INTERCEPTADOR FORTE (captura antes do link executar)
    document.addEventListener('click', function (e) {

        const btn = e.target.closest('.whatsapp');

        if (!btn) return;

        const ativo = localStorage.getItem('whatsAtivo') === 'true';

        if (!ativo) {
            e.preventDefault();
            e.stopPropagation(); // 🔥 garante que NÃO navega

            alert("🚫 Envio automático está DESATIVADO.");
        }

    }, true); // 🔥 TRUE = captura antes do navegador agir

});