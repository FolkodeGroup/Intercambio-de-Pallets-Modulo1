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

        // 🔹 Si ya se están mostrando todas las filas visibles, ocultar el botón
        botonVerMas.style.display = mostradas >= filasVisibles.length ? "none" : "";
    }

    function resetMostrarMas() {
        mostradas = LIMITE_INICIAL;
        actualizarTabla();
    }

    // =========================================================
    // 🔹 MENÚS (ordenar / filtrar)
    // =========================================================
    btnOrdenar.addEventListener("click", (e) => {
        e.stopPropagation();
        menuOrdenar.style.display = menuOrdenar.style.display === "none" ? "flex" : "none";
        menuTipo.style.display = "none";
    });

    btnTipo.addEventListener("click", (e) => {
        e.stopPropagation();
        menuTipo.style.display = menuTipo.style.display === "none" ? "flex" : "none";
        menuOrdenar.style.display = "none";
    });

    document.addEventListener("click", (e) => {
        if (!menuOrdenar.contains(e.target) && e.target !== btnOrdenar) {
            menuOrdenar.style.display = "none";
        }
        if (!menuTipo.contains(e.target) && e.target !== btnTipo) {
            menuTipo.style.display = "none";
        }
    });

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
            // Si el botón ya está activo, lo desactiva
            if (option.classList.contains('activo')) {
                option.classList.remove('activo');
                quitarFiltro(); // acá deshacés el filtro aplicado
            } else {
                // Si no está activo, lo activa
                option.classList.add('activo');
                aplicarFiltro(); // acá aplicás el filtro
            }
        });
    });

    // =========================================================
    // 🔹 FILTRAR
    // =========================================================
    menuTipo.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const tipo = option.dataset.tipo;

            // 🔸 Si se presiona el mismo filtro otra vez, se desactiva
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

    // Inicialización
    filtrarPorTipo(tabla, filtroActivo);
    actualizarTabla();
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
        const tipoCelda = fila.children[2].textContent.trim().toLowerCase();
        fila.style.display = (tipo === "todos" || tipoCelda === tipo) ? "" : "none";
    });
}
