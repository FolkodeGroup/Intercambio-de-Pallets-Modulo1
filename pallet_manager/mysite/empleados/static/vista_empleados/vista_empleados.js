document.addEventListener("DOMContentLoaded", ()=>{
    const btnVerMas = document.getElementById("btn-more");
    const filas = document.querySelectorAll("tbody tr.table-content-cels");
    const FILAS_POR_PASO = 8; // cuántas filas se muestran cada vez
    let visibles = FILAS_POR_PASO;

    // --- Ocultamos todas las filas que excedan el límite inicial
    filas.forEach((fila, index) => {
        if (index >= FILAS_POR_PASO) {
            fila.style.display = "none";
        }
    });

    // --- Al hacer clic en "Ver más"
    btnVerMas?.addEventListener("click", () => {
        const total = filas.length;
        const nuevasVisibles = visibles + FILAS_POR_PASO;

        filas.forEach((fila, index) => {
            if (index < nuevasVisibles) {
                fila.style.display = ""; // vuelve a mostrar la fila
            }
        });

        visibles = nuevasVisibles;

        // Si ya se muestran todas, ocultamos el botón
        if (visibles >= total) {
            btnVerMas.style.display = "none";
        }
    });

    // --- Ocultar botón si hay pocas filas
    if (filas.length <= FILAS_POR_PASO) {
        btnVerMas.style.display = "none";
    }

    document.querySelectorAll(".btn-cel-actions").forEach((btn) => {
        btn.addEventListener("click", (event) => {
            let menu = btn.nextElementSibling; 

            if (!menu) return;

            if(menu.classList.contains("active-actions")){
                menu.classList.remove("active-actions")
                return
            }
            // Ocultar todos los menús
            document.querySelectorAll(".menu-cel-actions").forEach(m => m.classList.remove("active-actions"));

            // Mostrar solo el menú de esta fila
            menu.classList.add("active-actions")
            
        });
    });
})