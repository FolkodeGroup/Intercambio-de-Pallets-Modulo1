//  Funcionalidad a los botones para "volver"

document.addEventListener("DOMContentLoaded", () => {
    const btnBack = document.getElementById('btn-back');
    btnBack.addEventListener('click', () => {
        window.history.back(); // Vuelve a la página anterior
    });
})