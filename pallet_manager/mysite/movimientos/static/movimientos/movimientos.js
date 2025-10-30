document.addEventListener("DOMContentLoaded", () => {
    const btnOrdenar = document.getElementById("ordenar-btn");
    const menuOrdenar = document.getElementById("menu-ordenar");
    const btnTipo = document.getElementById("filtro-btn");
    const menuTipo = document.getElementById("menu-tipo");
    const btnCelActions = document.querySelectorAll(".btn-cel-actions")
    const tabla = document.getElementById("tabla-movimientos");
    const botonVerMas = document.getElementById("btn-more");

    // definimos variables para cantidad inicial y el incremento de filas a mostrar
    const LIMITE_INICIAL = 7;
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
        botonVerMas.style.display = mostradas >= tabla.querySelectorAll("tbody tr").length ? "none" : "";
    }

    // =========================================================
    // 🔹 ORDENAR
    // =========================================================
    menuOrdenar.querySelectorAll("span").forEach((option) => {
        option.addEventListener("click", () => {
            const tipoOrden = option.dataset.orden;

            // Si el mismo filtro ya estaba activo → restaurar orden original
            if (option.classList.contains("ordenar-activo")) {
                option.classList.remove("ordenar-activo");
                restaurarOrdenOriginal(tabla);
            } else {
                // Quitar la clase 'ordenar-activo' de los demás
                menuOrdenar.querySelectorAll("span").forEach(s => s.classList.remove("ordenar-activo"));

                // Activar el filtro actual
                option.classList.add("ordenar-activo");

                // Aplicar el orden según el criterio
                if (tipoOrden === "sin-filtros") {
                    restaurarOrdenOriginal(tabla);
                } else {
                    ordenarPorCriterio(tabla, tipoOrden);
                }
            }

            menuOrdenar.style.display = "none";
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
            if (tipo === "todos" || filtroActivo === tipo) {
                filtroActivo = "todos";
                restaurarOrdenOriginal(tabla);
                resetMostrarMas();
                
            } else {
                filtroActivo = tipo;
                option.classList.add("activo");
                // Aplicar el filtro inmediatamente
                filtrarPorTipo(tabla, filtroActivo);
            }

            
            
            menuTipo.style.display = "none";
        });
    });

    // =========================================================
    // 🔹 BOTÓN "VER MÁS"
    // =========================================================

    botonVerMas.addEventListener("click", () => {
        const filas = Array.from(tabla.querySelectorAll("tbody tr"));
        const filasNoVisibles = filas.filter(f => f.style.display === "none");

        // Aumentar la cantidad mostrada
        mostradas += LIMITE_INICIAL;

        filasNoVisibles.forEach((fila, i) => {
            fila.style.display = i < mostradas ? "" : "block";
        });

        // Ocultar el botón si ya no hay más filas ocultas
        botonVerMas.style.display = mostradas >= filasNoVisibles.length ? "none" : "";
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

function ordenarPorCriterio(table, criterio) {
    const colMap = {
        empresa: 0,     // 🔧 ajustá estos índices al orden real de tus columnas
        fecha: 1,
        tipo: 2,
        cantidad: 3,
        responsable: 4
    };

    const colIndex = colMap[criterio];
    if (colIndex === undefined) return;

    const tbody = table.querySelector("tbody");
    let rows = Array.from(tbody.querySelectorAll("tr"));

    // 🔹 Dirección por defecto según el criterio
    let isDesc = false;
    if (criterio === "cantidad" || criterio === "fecha") isDesc = true;

    rows.sort((a, b) => {
        const cellA = a.children[colIndex].textContent.trim();
        const cellB = b.children[colIndex].textContent.trim();

        const numA = parseFloat(cellA.replace(",", "."));
        const numB = parseFloat(cellB.replace(",", "."));
        if (!isNaN(numA) && !isNaN(numB)) {
            return isDesc ? numB - numA : numA - numB;
        }

        const dateA = Date.parse(cellA);
        const dateB = Date.parse(cellB);
        if (!isNaN(dateA) && !isNaN(dateB)) {
            return isDesc ? dateB - dateA : dateA - dateB;
        }

        return isDesc ? cellB.localeCompare(cellA) : cellA.localeCompare(cellB);
    });

    tbody.innerHTML = "";
    rows.forEach(r => tbody.appendChild(r));
}

// Guardar el orden original al cargar
document.addEventListener("DOMContentLoaded", () => {
    const tbody = document.querySelector("#tabla-movimientos tbody");
    if (tbody) {
        // Guardamos una copia del orden original de las filas
        window.ordenOriginal = Array.from(tbody.querySelectorAll("tr")).map(tr => tr.cloneNode(true));
    }
});

function restaurarOrdenOriginal(table) {
    if (!window.ordenOriginal) return;

    const tbody = table.querySelector("tbody");
    tbody.innerHTML = "";

    // Clonamos nuevamente las filas originales para evitar referencias rotas
    window.ordenOriginal.forEach(tr => tbody.appendChild(tr.cloneNode(true)));
}
// =========================================================
// 🔸 FILTRAR TABLA
// =========================================================
function filtrarPorTipo(table, tipo) {
    const filas = table.querySelectorAll("tbody tr");

    if (filas.length === 0) return;

    filas.forEach(fila => {
        if (fila) {
            const tipoCelda = fila.children[2].textContent.trim().toLowerCase(); // columna tipo

            if(tipo === "egreso"){
                fila.style.display = (tipo === "todos" || tipoCelda === "out") ? "" : "none";
            }else if(tipo === "ingreso"){
                fila.style.display = (tipo === "todos" || tipoCelda === "in") ? "" : "none";
            }
        }
        
    });
}


