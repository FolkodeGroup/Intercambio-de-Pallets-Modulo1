document.addEventListener("DOMContentLoaded", () => {
    const btnOrdenar = document.getElementById("ordenar-btn");
    const menuOrdenar = document.getElementById("menu-ordenar");

    const btnTipo = document.getElementById("filtro-btn");
    const menuTipo = document.getElementById("menu-tipo");

    const tabla = document.getElementById("tabla-movimientos");

    // 🔹 Mostrar / ocultar menú de ordenar
    btnOrdenar.addEventListener("click", (e) => {
        e.stopPropagation();
        menuOrdenar.style.display = menuOrdenar.style.display === "none" ? "flex" : "none";
        menuTipo.style.display = "none"; // cerrar el otro menú si está abierto
    });

    // 🔹 Mostrar / ocultar menú de tipo
    btnTipo.addEventListener("click", (e) => {
        e.stopPropagation();
        menuTipo.style.display = menuTipo.style.display === "none" ? "flex" : "none";
        menuOrdenar.style.display = "none"; // cerrar el otro menú
    });

    // 🔹 Cerrar menús al hacer clic fuera
    document.addEventListener("click", (e) => {
        if (!menuOrdenar.contains(e.target) && e.target !== btnOrdenar) {
            menuOrdenar.style.display = "none";
        }
        if (!menuTipo.contains(e.target) && e.target !== btnTipo) {
            menuTipo.style.display = "none";
        }
    });

    // 🔹 Ordenar al hacer clic en un span
    menuOrdenar.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const colIndex = parseInt(option.dataset.col);
            sortTable(tabla, colIndex);
            menuOrdenar.style.display = "none";

            // Quitar clase activa de todos los spans
            menuOrdenar.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
            // Agregar clase al filtro actual
            option.classList.add("activo");
        });
    });

    // 🔹 Filtrar por tipo (Ingreso / Egreso)
    menuTipo.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const tipo = option.dataset.tipo;
            filtrarPorTipo(tabla, tipo);
            menuTipo.style.display = "none";

            // Quitar clase activa de todos los spans
            menuTipo.querySelectorAll("span").forEach(s => s.classList.remove("activo"));
            // Marcar el filtro actual
            option.classList.add("activo");
        });
    });
});

// 🔸 Función para ordenar tabla
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

    rows.forEach((r) => tbody.appendChild(r));
}

// 🔸 Función para filtrar por tipo (Ingreso/Egreso)
function filtrarPorTipo(table, tipo) {
    const filas = table.querySelectorAll("tbody tr");
    filas.forEach(fila => {
        const tipoCelda = fila.children[2].textContent.trim().toLowerCase();
        if (tipo === "todos" || tipoCelda === tipo) {
            fila.style.display = "";
        } else {
            fila.style.display = "none";
        }
    });
}

// 🔸 Mostrar más filas
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

        if (mostradas >= filas.length) {
            boton.style.display = "none";
        }
    }

    boton.addEventListener("click", () => {
        mostradas += INCREMENTO;
        actualizarTabla();
    });

    actualizarTabla();
});
