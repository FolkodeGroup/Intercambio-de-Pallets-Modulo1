document.addEventListener("DOMContentLoaded", () => {
    const btnOrdenar = document.getElementById("ordenar-btn");
    const menuOrdenar = document.getElementById("menu-ordenar");
    const btnTipo = document.getElementById("filtro-btn");
    const menuTipo = document.getElementById("menu-tipo");
    const btnCelActions = document.querySelectorAll(".btn-cel-actions")
    const tabla = document.getElementById("tabla-movimientos");
    const botonVerMas = document.getElementById("btn-more");

    const LIMITE_INICIAL = 8;
    const INCREMENTO = 10;
    let mostradas = LIMITE_INICIAL;
    let filtroActivo = "todos"; // 🔸 Filtro actual

    // función para mostrar/ocultar menu de la barra de filtros
    function toggleMenu(boton, menu, otrosMenus = []) {
        menu.style.display = "none";

        boton.addEventListener("click", (e) => {
            e.stopPropagation();
            const isVisible = menu.style.display !== "none";
            menu.style.display = isVisible ? "none" : "flex";

            // Ocultar otros menús pasados como array
            otrosMenus.forEach(m => m.style.display = "none");
        });

        // Cerrar menú al hacer click fuera
        document.addEventListener("click", (e) => {
            if (!menu.contains(e.target) && e.target !== boton) {
                menu.style.display = "none";
            }
        });
    }

    toggleMenu(btnOrdenar, menuOrdenar, [menuTipo]);
    toggleMenu(btnTipo, menuTipo, [menuOrdenar]);

    // =========================================================
    // 🔸 FUNCIONES AUXILIARES
    // =========================================================
    function actualizarTabla() {
        const filas = Array.from(tabla.querySelectorAll("tbody tr"));
        const filasVisibles = filas.filter(f => f.style.display !== "none");

        filasVisibles.forEach((fila, i) => {
            fila.style.display = i < mostradas ? "" : "none";
        });

        botonVerMas.style.display = mostradas >= filasVisibles.length ? "none" : "";
    }

    function resetMostrarMas() {
        mostradas = LIMITE_INICIAL;
        actualizarTabla();
    }

    // =========================================================
    // 🔹 ORDENAR
    // =========================================================
    menuOrdenar.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const colIndex = parseInt(option.dataset.col);
            sortTable(tabla, colIndex);
            menuOrdenar.style.display = "none";

            // Toggle visual de selección
            menuOrdenar.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
            if (option.classList.contains('activo')) {
                option.classList.remove('activo');
            } else {
                option.classList.add('activo');
            }
        });
    });

    // =========================================================
    // 🔹 FILTRAR
    // =========================================================
    menuTipo.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const tipo = option.dataset.tipo;

            // Quitar la clase 'activo' de todos los spans primero
            menuTipo.querySelectorAll("span").forEach(s => s.classList.remove("activo"));

            // Si el mismo filtro ya estaba activo → mostrar todos
            if (filtroActivo === tipo) {
                filtroActivo = "todos";
            } else {
                filtroActivo = tipo;
                option.classList.add("activo");
            }

            // Aplicar el filtro inmediatamente
            filtrarPorTipo(tabla, filtroActivo);
            resetMostrarMas();
            menuTipo.style.display = "none";
        });
    });

    // =========================================================
    // 🔹 BOTÓN "VER MÁS"
    // =========================================================

    botonVerMas.addEventListener("click", () => {
        mostradas += INCREMENTO;
        actualizarTabla();
    });

    // =========================================================
    // 🔹 INICIALIZACIÓN
    // =========================================================
    // Eliminamos cualquier filtro que esté activo al iniciar la página
    const filas = tabla.querySelectorAll("tbody tr");
    if (filas.length > 0) {
        filtroActivo = "todos";
        filtrarPorTipo(tabla, filtroActivo);
        actualizarTabla();
        
        // Quitar la clase activo de las opciones del menú de tipo
        menuTipo.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
    }
    document.querySelectorAll(".btn-cel-actions").forEach((btn) => {
        btn.addEventListener("click", (event) => {
            let menu = btn.nextElementSibling; 
            console.log(menu)
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
});

// =========================================================
// 🔸 ORDENAR TABLA
// =========================================================
function sortTable(table, colIndex) {
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    const isAsc = table.dataset.sortCol == colIndex && table.dataset.sortDir === "asc";
    table.dataset.sortCol = colIndex;
    table.dataset.sortDir = isAsc ? "desc" : "asc";

    rows.sort((a, b) => {
        const cellA = a.children[colIndex].textContent.trim();
        const cellB = b.children[colIndex].textContent.trim();

        const numA = parseFloat(cellA.replace(",", "."));
        const numB = parseFloat(cellB.replace(",", "."));
        if (!isNaN(numA) && !isNaN(numB)) return isAsc ? numA - numB : numB - numA;

        const dateA = Date.parse(cellA);
        const dateB = Date.parse(cellB);
        if (!isNaN(dateA) && !isNaN(dateB)) return isAsc ? dateA - dateB : dateB - dateA;

        return isAsc ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
    });

    rows.forEach(r => tbody.appendChild(r));
}

// =========================================================
// 🔸 FILTRAR TABLA
// =========================================================
function filtrarPorTipo(table, tipo) {
    const filas = table.querySelectorAll("tbody tr");
    filas.forEach(fila => {
        if (fila) {
            const tipoCelda = fila.children[2].textContent.trim().toLowerCase(); // columna tipo
            fila.style.display = (tipo === "todos" || tipoCelda === tipo) ? "" : "none";
        }
        
    });
}