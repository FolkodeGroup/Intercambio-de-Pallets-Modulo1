document.addEventListener("DOMContentLoaded", () => {
    const btnOrdenar = document.getElementById("ordenar-btn");
    const menuOrdenar = document.getElementById("menu-ordenar");

    const btnTipo = document.getElementById("filtro-btn");
    const menuTipo = document.getElementById("menu-tipo");

    const tabla = document.getElementById("tabla-movimientos");
    const botonVerMas = document.getElementById("btn-more");

    const LIMITE_INICIAL = 8;
    const INCREMENTO = 10;
    let mostradas = LIMITE_INICIAL;
    let filtroActivo = "todos"; // 🔸 Filtro actual

    // =========================================================
    // 🔸 TOGGLE MENÚ GENÉRICO
    // =========================================================
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
                quitarFiltro(); // función externa que deshace filtro aplicado
            } else {
                option.classList.add('activo');
                aplicarFiltro(); // función externa que aplica filtro
            }
        });
    });

    // =========================================================
    // 🔹 FILTRAR
    // =========================================================
    menuTipo.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const tipo = option.dataset.tipo;

            if (filtroActivo === tipo) {
                filtroActivo = "todos";
                menuTipo.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
            } else {
                filtroActivo = tipo;
                menuTipo.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
                option.classList.add("activo");
            }

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
    const filas = tabla.querySelectorAll("tbody tr");
    if (filas.length > 0) {
        filtrarPorTipo(tabla, filtroActivo);
        actualizarTabla();
    }
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


