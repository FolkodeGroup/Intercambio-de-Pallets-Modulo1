document.addEventListener('DOMContentLoaded', function(){
  const btnOperation = document.getElementById('btn-operation');
  const btnCancelForm = document.querySelector('.form-btn-cancel');
  const formStock = document.querySelector('.form-stock');
  
  btnCancelForm.addEventListener('click', ()=>{
    formStock.style.display = 'none';
    formStock.reset();
  });

  btnOperation.addEventListener('click', ()=>{
    const formStyle = window.getComputedStyle(formStock);
    if(formStyle.display === 'none'){
      formStock.style.display = 'flex';
    }
  });

  formStock.addEventListener('submit', function(e){
    e.preventDefault();
  });

  (function(){
    function getCookie(name){
      let v=null;if(document.cookie&&document.cookie!==''){
        const c=document.cookie.split(';');
        for(let i=0;i<c.length;i++){const ck=c[i].trim();
          if(ck.substring(0,name.length+1)===(name+'=')){v=decodeURIComponent(ck.substring(name.length+1));break;}
        }
      } return v;
    }
    const csrftoken = getCookie('csrftoken');

    // POST por nombre de URL (namespace movimientos)

    const POST_URL = formStock.dataset.postUrl;

    function refreshUI(stock, counters){
      const tbody = document.getElementById('tbody-stock');
      tbody.innerHTML = '';
      if (!stock || !stock.length){
        tbody.innerHTML = '<tr><td colspan="5">Sin datos de stock.</td></tr>';
      } else {
        stock.forEach(s => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td>${s.tipo}</td>
            <td>${s.total}</td>
            <td>${s.disponibles}</td>
            <td>${s.en_uso}</td>
            <td>${s.danados}</td>`;
          tbody.appendChild(tr);
        });
      }
      // actualizar números dentro de los donuts
      const t = document.querySelectorAll('.donut text');
      if(t.length>=3){
        t[0].textContent = (counters && counters.disponibles) || 0;
        t[1].textContent = (counters && counters.en_uso) || 0;
        t[2].textContent = (counters && counters.danados) || 0;
      }
    }

    const btnAgregar = document.getElementById('btn-agregar');
    const modalEl = document.getElementById('confirmModal');
    const confirmText = document.getElementById('confirm-text');
    const btnConfirmar = document.getElementById('btn-confirmar');
    const toastEl = document.getElementById('toast');
    const toastBody = document.getElementById('toast-body');
    const bsModal = new bootstrap.Modal(modalEl);
    const bsToast = new bootstrap.Toast(toastEl);

    btnAgregar.addEventListener('click', function(){
      const op = document.getElementById('fld-operacion').value;
      const sel = document.getElementById('fld-tipo');
      const tipoNombre = sel.options[sel.selectedIndex]?.dataset?.name || sel.options[sel.selectedIndex]?.textContent || '—';
      const tipoId = sel.value;
      const cantidad = parseInt(document.getElementById('fld-cantidad').value || '0');

      if(!cantidad || cantidad<=0){ toastBody.textContent = "Ingresá una cantidad válida."; bsToast.show(); return; }
      if(!tipoId){ toastBody.textContent = "Seleccioná un tipo válido."; bsToast.show(); return; }

      confirmText.textContent = `¿Confirmás ${op==='IN'?'INGRESAR':'EGRESAR'} ${cantidad} pallet(s) del tipo “${tipoNombre}”?`;
      bsModal.show();

      btnConfirmar.replaceWith(btnConfirmar.cloneNode(true));
      const newBtn = document.getElementById('btn-confirmar');

      newBtn.addEventListener('click', async function() {
        newBtn.disabled = true;
        try {
          const form = new FormData();
          form.append('operacion', op);
          form.append('tipo_pallet_id', tipoId);
          form.append('cantidad', cantidad);

          const resp = await fetch(POST_URL, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
            body: form
          });

          let data = null, text = '';
          try { data = await resp.clone().json(); } catch { text = await resp.text(); }

          if(!resp.ok || !data?.ok){
            const msg = (data && data.error) ? data.error : (text || `HTTP ${resp.status}`);
            throw new Error(msg);
          }

          refreshUI(data.stock, data.contadores);
          toastBody.textContent = "Operación realizada con éxito.";
          bsToast.show();
          bsModal.hide(); // Cerramos solo si todo salió OK
          formStock.reset()
          formStock.style.display = "none"
        } catch(err){
          toastBody.textContent = "Error: " + (err?.message || err);
          bsToast.show(); // Modal sigue abierto para poder corregir
        } finally {
          newBtn.disabled = false;
        }
      });
    });
  })();
});
