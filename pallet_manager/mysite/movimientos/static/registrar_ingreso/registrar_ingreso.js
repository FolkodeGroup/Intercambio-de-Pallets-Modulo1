//  Funcionalidad a los botones para "volver"
const btnBack = document.querySelector("#btn-back");
btnBack.addEventListener('click', () => {
    window.history.back();
});