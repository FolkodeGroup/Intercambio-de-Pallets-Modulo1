// Esperamos a que cargue todo el contenido de la página para ejecutar el codigo
document.addEventListener("DOMContentLoaded", () => {
  const btnEgreso = document.getElementById('btn-egreso')
  const btnBack = document.getElementById('btn-back');
    btnBack.addEventListener('click', () => {
        window.history.back(); // Vuelve a la página anterior
    });

    // Confirmación (opcional) similar a Ingreso
    function getVal(name) {
      const el = document.getElementsByName(name)[0];
      if (!el) return '';
      if (el.tagName === 'SELECT') {
        return el.options[el.selectedIndex]?.text || el.value || '';
      }
      return el.value || '';
    }

    function totalUnidades() {
      const totalForms = parseInt(getVal('form-TOTAL_FORMS')) || 0;
      let total = 0;
      for (let i = 0; i < totalForms; i++) {
        const del = document.getElementsByName(`form-${i}-DELETE`)[0];
        if (del && del.checked) continue;
        const cant = parseInt(document.getElementsByName(`form-${i}-cantidad`)[0]?.value || '0') || 0;
        total += cant;
      }
      return total;
    }

    function confirmarEgreso() {
      const empresa = getVal('empresa') || '(sin cliente)';
      const total = totalUnidades();
      return window.confirm(
        "¿Confirmar el egreso?\n\n" +
        "Cliente: " + empresa + "\n" +
        "Unidades totales: " + total + "\n\n" +
        "Si estás segura/o, presioná Aceptar para guardar."
      );
    }
    
    btnEgreso.addEventListener('click', confirmarEgreso)
})