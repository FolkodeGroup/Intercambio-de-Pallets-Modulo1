
document.addEventListener("DOMContentLoaded", function () {
    const filas = Array.from(document.querySelectorAll("#tabla-movimientos tbody tr"));
    const boton = document.getElementById("btn-more");

    const LIMITE_INICIAL = 8;
    const INCREMENTO = 10;
    let mostradas = LIMITE_INICIAL;

    function actualizarTabla() {
      filas.forEach((fila, i) => {
        fila.style.display = i < mostradas ? "" : "none";
      });

      // Si no hay más filas ocultas, ocultar el botón
      if (mostradas >= filas.length) {
        boton.style.display = "none";
      }
    }

    boton.addEventListener("click", () => {
      mostradas += INCREMENTO;
      actualizarTabla();
    });

    // Mostrar solo las primeras al cargar
    actualizarTabla();
  });