const resultados = document.getElementById('resultados_personas');
const mapDiv = document.getElementById('mapDiv');
let map;
// Función para filtrar clientes según el input
function filtrarClientes(inputId, listaId, tipo) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const lista = document.getElementById(listaId);
    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar llamada para obtener los clientes filtrados
    fetch("/bitacora/filtrar_clientes", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ query: filter })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (tipo === 'intervienen') {
                lista.innerHTML = "";
                if (input.value != "") {
                    if (data.clientes.length > 0) {
                        lista.style.display = "block";  // Mostrar el div
                        data.clientes.forEach(cliente => {
                            const div = document.createElement("div");
                            div.classList.add("list-group-item");
                            div.textContent = `${cliente.nombre} - ${cliente.identificacion}`;
                            div.onclick = () => seleccionarCliente(cliente, listaId, tipo);
                            lista.appendChild(div);
                        });
                        deshabilitarClientesSeleccionados(data);
                    }
                } else {
                    lista.innerHTML = "";
                    lista.style.display = "none";  // Ocultar el div si no hay resultados
                }
            } else if (tipo === 'responsable') {
                const resultados = document.getElementById('resultados_responsable');
                resultados.innerHTML = "";
                if (input.value != "") {
                    if (data.clientes.length > 0) {
                        resultados.style.display = "block";  // Mostrar el div
                        data.clientes.forEach(cliente => {
                            const div = document.createElement("div");
                            div.classList.add("list-group-item");
                            div.textContent = `${cliente.nombre} - ${cliente.identificacion}`;
                            div.onclick = () => seleccionarResponsable(cliente, inputId);
                            resultados.appendChild(div);
                        });
                    }
                } else {
                    resultados.style.display = "none";  // Ocultar el div si no hay resultados
                }
            }
        })
        .catch(error => {
            console.error("Error al obtener clientes:", error);
        });
}

function deshabilitarClientesSeleccionados(data) {
    const listaClientes = document.getElementById('lista_personas').getElementsByTagName('li');
    data.clientes.forEach(cliente => {
        for (let i = 0; i < listaClientes.length; i++) {
            const nombreElemento = listaClientes[i].querySelector('.nombre-persona').innerText.trim();
            if (nombreElemento === cliente.nombre.trim()) {
                const resultItems = document.querySelectorAll('#resultados_personas .list-group-item');
                resultItems.forEach(resultItem => {
                    if (resultItem.textContent.includes(cliente.nombre)) {
                        resultItem.classList.add("disabled");
                    }
                });
            }
        }
    });
}

function seleccionarCliente(cliente, listaId, tipo) {
    if (tipo === 'intervienen') {
        seleccionarIntervienen(cliente, 'lista_personas');
    } else if (tipo === 'responsable') {
        seleccionarResponsable(cliente, listaId);
    }
}

function seleccionarIntervienen(cliente, listaId) {
    const lista = document.getElementById(listaId);

    // Verificar si el cliente ya está en la lista
    const existingItem = lista.querySelector(`li[data-identificacion="${cliente.identificacion}"]`);
    if (existingItem) {
        return; // Si el cliente ya está en la lista, no hacer nada
    }

    const li = document.createElement("li");
    li.classList.add("list-group-item");
    const divInfo = document.createElement("div");
    divInfo.classList.add("d-flex", "justify-content-between", "align-items-center");
    const divText = document.createElement("div");
    divText.innerHTML = `        
        <div><strong>Nro. de identificación:</strong> <span class="identificacion-persona">${cliente.identificacion}</span></div>
        <div><strong>Nombre:</strong> <span class="nombre-persona">${cliente.nombre}</span></div>
    `;

    const btnEliminar = document.createElement("button");
    btnEliminar.classList.add("btn-clear");
    btnEliminar.innerHTML = "<i class='bx bx-trash-alt'></i>";
    btnEliminar.onclick = () => eliminar(li, listaId, null);
    divInfo.appendChild(divText);
    divInfo.appendChild(btnEliminar);
    li.appendChild(divInfo);
    lista.appendChild(li);

    // Limpiar el campo de búsqueda y los resultados
    document.getElementById('buscar_personas').value = "";
    const resultados = document.getElementById('resultados_personas');
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar los resultados

    actualizarPersonasJson();  // Actualizar la lista de personas
}

function seleccionarResponsable(cliente, inputId) {
    const input = document.getElementById('buscar_responsable');
    const inputNombre = document.getElementById('nombre_encargado');
    input.value = cliente.identificacion;
    inputNombre.value = cliente.nombre;
    input.readOnly = true;
    inputNombre.readOnly = true;

    // Eliminar botón de eliminar anterior, si existe
    const btnEliminarPrev = inputNombre.parentNode.querySelector('.btn-clear-R');
    if (btnEliminarPrev) {
        btnEliminarPrev.remove();
    }

    const btnEliminar = document.createElement("button");
    btnEliminar.classList.add("btn-clear-R");
    btnEliminar.innerHTML = "<i class='bx bx-trash-alt'></i>";
    btnEliminar.onclick = () => eliminarResponsable(input, inputNombre);
    inputNombre.parentNode.appendChild(btnEliminar);

    // Limpiar el campo de búsqueda y los resultados
    document.getElementById('resultados_responsable').value = "";
    const resultados = document.getElementById('resultados_responsable');
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
}

function eliminar(elemento, listaId, inputId) {
    const lista = document.getElementById(listaId);
    if (inputId != null) {
        inputId.readOnly = false;
    }
    lista.removeChild(elemento);
    actualizarPersonasJson();
    actualizarHerramientasJson();
    eliminarZonaMapa();
}

function eliminarZonaMapa() {
    if (map.getSource('area')) {
        // Primero eliminar las capas asociadas si existen
        if (map.getLayer('area')) {
            map.removeLayer('area');
        }
        if (map.getLayer('area-outline')) {
            map.removeLayer('area-outline');
        }

        // Luego eliminar la fuente
        map.removeSource('area');
        mapDiv.style.display = "none";
    }
}

function actualizarPersonasJson() {
    const listaPersonas = [];
    const lista = document.getElementById('lista_personas');
    lista.querySelectorAll('li').forEach(item => {
        const nombre = item.querySelector('.nombre-persona').innerText.trim();
        const identificacion = item.querySelector('.identificacion-persona').innerText.trim();

        listaPersonas.push({
            nombre: nombre,
            identificacion: identificacion
        });
    });

    document.getElementById('personas_json').value = listaPersonas; // Almacena como string
    console.log(document.getElementById('personas_json').value);
}

function eliminarResponsable(inputId, inputNombre) {
    inputId.value = "";
    inputNombre.value = "";
    inputId.readOnly = false;
    inputNombre.readOnly = false;
    const btnEliminar = inputNombre.parentNode.querySelector('.btn-clear-R');
    if (btnEliminar) {
        btnEliminar.remove();
    }
}

//herramientas
function filtrarHerramientas(inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const lista = document.getElementById(listaId);

    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar llamada para obtener los clientes filtrados
    fetch("/bitacora/filtrar_herramientas", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ query: filter })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            lista.innerHTML = "";
            if (input.value != "") {
                if (data.herramientas.length > 0) {
                    lista.style.display = "block";  // Mostrar el div
                    data.herramientas.forEach(herramienta => {
                        const div = document.createElement("div");
                        div.classList.add("list-group-item");
                        div.textContent = `${herramienta.nombre} - ${herramienta.funcionalidad}`;
                        div.onclick = () => seleccionarHerramienta(herramienta, 'lista_herramientas');
                        lista.appendChild(div);
                    });

                    // Deshabilitar los herramientas ya seleccionados
                    const listaHerramientas = document.getElementById('lista_herramientas').getElementsByTagName('li');
                    data.herramientas.forEach(herramienta => {
                        for (let i = 0; i < listaHerramientas.length; i++) {
                            const nombreElemento = listaHerramientas[i].querySelector('div strong').nextSibling.nodeValue.trim();
                            if (nombreElemento && nombreElemento.trim() === herramienta.nombre) {
                                const resultItems = document.querySelectorAll('#resultados_herramientas .list-group-item');
                                for (let resultItem of resultItems) {
                                    if (resultItem.textContent.includes(herramienta.nombre)) {
                                        resultItem.classList.add("disabled");
                                    }
                                }
                            }
                        }
                    });
                }
            } else {
                lista.innerHTML = "";
                lista.style.display = "none";  // Ocultar el div si no hay resultados
            }
        })
        .catch(error => {
            console.error("Error al obtener herramientas:", error);
        });
}

function seleccionarHerramienta(herramienta, listaId) {
    const lista = document.getElementById(listaId);

    // Verificar si el herramienta ya está en la lista
    const items = lista.getElementsByTagName('li');
    for (let i = 0; i < items.length; i++) {
        const nombreElemento = items[i].querySelector('div strong').nextSibling.nodeValue.trim();
        if (nombreElemento === herramienta.nombre) {
            return; // Si la herramienta ya está en la lista, no hacer nada
        }
    }

    const li = document.createElement("li");
    li.classList.add("list-group-item");

    const divInfo = document.createElement("div");
    divInfo.classList.add("d-flex", "justify-content-between", "align-items-center");

    const divText = document.createElement("div");
    divText.innerHTML = `
        <div><strong>Nombre de equipo:</strong> <span class="nombre-equipo">${herramienta.nombre}</span></div>
        <div><strong>Funcionalidad:</strong> <span class="funcionalidad-equipo">${herramienta.funcionalidad}</span></div>
    `;
    const btnEliminar = document.createElement("button");
    btnEliminar.classList.add("btn-clear");
    btnEliminar.innerHTML = "<i class='bx bx-trash-alt'></i>";
    btnEliminar.onclick = () => eliminar(li, listaId, null);
    divInfo.appendChild(divText);
    divInfo.appendChild(btnEliminar);

    li.appendChild(divInfo);
    lista.appendChild(li);


    // Limpiar el campo de búsqueda y los resultados
    document.getElementById('buscar_herramientas').value = "";
    const resultados = document.getElementById('resultados_herramientas');
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el di

    actualizarHerramientasJson();

}

function actualizarHerramientasJson() {
    const listaHerramientas = document.getElementById('lista_herramientas');
    const listHerramientas = [];
    listaHerramientas.querySelectorAll('li').forEach(item => {
        const nombre = item.querySelector('.nombre-equipo').textContent.trim();
        const funcionalidad = item.querySelector('.funcionalidad-equipo').textContent.trim();
        listHerramientas.push({
            nombre: nombre,
            funcionalidad: funcionalidad
        });
    });
    document.getElementById('equipos_json').value = JSON.stringify(listHerramientas);
    console.log(document.getElementById('equipos_json').value = JSON.stringify(listHerramientas));
}


//Zonas

function filtrarZonas(inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const lista = document.getElementById(listaId);

    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar llamada para obtener los clientes filtrados
    fetch("/bitacora/filtrar_zonas", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ query: filter })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            lista.innerHTML = "";
            if (input.value != "") {
                if (data.zonas.length > 0) {
                    lista.style.display = "block";  // Mostrar el div
                    data.zonas.forEach(zona => {
                        const div = document.createElement("div");
                        div.classList.add("list-group-item");
                        div.textContent = `${zona.nombre}`;
                        div.onclick = () => seleccionarZona(zona, 'lista_zonas', input);
                        lista.appendChild(div);
                    });

                    // Deshabilitar los herramientas ya seleccionados
                    const listaZonas = document.getElementById('lista_zonas').getElementsByTagName('li');
                    data.zonas.forEach(zona => {
                        for (let i = 0; i < listaZonas.length; i++) {
                            const nombreElemento = listaZonas[i].querySelector('div strong').nextSibling.nodeValue.trim();
                            if (nombreElemento && nombreElemento.trim() === zona.nombre) {
                                const resultItems = document.querySelectorAll('#resultados_zonas .list-group-item');
                                for (let resultItem of resultItems) {
                                    if (resultItem.textContent.includes(zona.nombre)) {
                                        resultItem.classList.add("disabled");
                                    }
                                }
                            }
                        }
                    });
                }
            } else {
                lista.innerHTML = "";
                lista.style.display = "none";  // Ocultar el div si no hay resultados
            }
        })
        .catch(error => {
            console.error("Error al obtener zonas:", error);
        });
}

function seleccionarZona(zona, listaId, input) {
    const lista = document.getElementById(listaId);

    // Verificar si el zona ya está en la lista
    const items = lista.getElementsByTagName('li');
    for (let i = 0; i < items.length; i++) {
        const nombreElemento = items[i].querySelector('div strong').nextSibling.nodeValue.trim();
        if (nombreElemento === zona.nombre) {
            return; // Si la zona ya está en la lista, no hacer nada
        }
    }

    const li = document.createElement("li");
    li.classList.add("list-group-item");

    const divHeader = document.createElement("div");
    divHeader.classList.add("zona-header");
    divHeader.innerHTML = `
        <div>
            <strong>Nombre de zona:</strong> ${zona.nombre} <br>
            <strong>Parcelas:</strong> ${zona.lista_parcelas.length}
        </div>
        <button class="btn-clear"><i class='bx bx-trash-alt'></i></button>
    `;

    const divBody = document.createElement("div");
    divBody.classList.add("zona-body");
    divBody.id = `zona-body-${zona.nombre}`;
    divBody.appendChild(generarListaParcelas(zona.lista_parcelas, zona));

    // Asignar eventos de clic
    divHeader.querySelector('.btn-clear').onclick = (e) => {
        e.stopPropagation();  // Evitar que se propague al divHeader
        eliminar(li, listaId, input);
    };

    divHeader.querySelector('div').onclick = () => toggleZonaBody(zona.nombre);


    li.appendChild(divHeader);
    li.appendChild(divBody);
    lista.appendChild(li);


    // Limpiar el campo de búsqueda y los resultados
    document.getElementById('buscar_zonas').value = "";
    const resultados = document.getElementById('resultados_zonas');
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
    input.readOnly = true;
    inicializarMapa(zona);
}

function inicializarMapa(zona) {
    mapDiv.style.display = "block";

    if (!map) {
        map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/hybrid/style.json?key=A1mAVA0b8Lsf3DtgWE85',
            center: [-75.4794, 10.3910],
            zoom: 12
        });

        map.on('load', () => {
            console.log("Mapa cargado, mostrando zona y parcelas...");

            // Aseguramos que el estilo del mapa está completamente cargado antes de agregar capas
            if (map.isStyleLoaded()) {
                mostrarZonaGuardada(zona, map);
            } else {
                map.once('styledata', () => {
                    mostrarZonaGuardada(zona, map);
                });
            }
        });

        map.on('error', (e) => {
            console.error("Error al cargar el mapa: ", e);
        });
    } else {
        // Si el mapa ya está inicializado, simplemente muestra la nueva zona
        mostrarZonaGuardada(zona, map);
        map.resize();
    }

}

function mostrarZonaGuardada(zona, map) {
    const coordinates = JSON.parse(zona.coordenadas_area);

    if (coordinates && coordinates.length > 0) {
        const areaFeature = {
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: [coordinates]
            }
        };

        if (map.getSource('area')) {
            // Primero eliminar las capas asociadas si existen
            if (map.getLayer('area')) {
                map.removeLayer('area');
            }
            if (map.getLayer('area-outline')) {
                map.removeLayer('area-outline');
            }

            // Luego eliminar la fuente
            map.removeSource('area');
        }

        // Ahora añadir la fuente y las capas de nuevo
        map.addSource('area', {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [areaFeature]
            }
        });

        map.addLayer({
            id: 'area',
            type: 'fill',
            source: 'area',
            layout: {},
            paint: {
                'fill-color': '#888888',
                'fill-opacity': 0.4
            }
        });

        map.addLayer({
            id: 'area-outline',
            type: 'line',
            source: 'area',
            layout: {},
            paint: {
                'line-color': '#000000',
                'line-width': 2
            }
        });

        map.flyTo({ center: coordinates[0], zoom: 12 }); // Ajustar la vista del mapa a la zona
    } else {
        console.error('No se encontraron coordenadas válidas en la zona.');
    }
}

function toggleZonaBody(nombreZona) {
    const zonaBody = document.getElementById(`zona-body-${nombreZona}`);
    if (zonaBody.style.display === "none" || zonaBody.style.display === "") {
        zonaBody.style.display = "block";
    } else {
        zonaBody.style.display = "none";
    }
}

function generarListaParcelas(parcelas, zona) {
    const parcelasList = document.createElement("div");

    parcelas.forEach((parcela, index) => {
        const parcelItem = document.createElement("div");
        parcelItem.classList.add("parcel-list-item", "d-flex", "justify-content-between", "align-items-center");

        // Inicializa el estado de ocupada a false si no está definido
        if (typeof parcela.ocupada === 'undefined') {
            parcela.ocupada = false;
        }

        const parcelInfo = document.createElement("div");
        parcelInfo.innerHTML = `
            <div class="parcel-status">
                <input type="checkbox" id="parcela-${index}" ${parcela.ocupada ? 'checked' : ''}> ${parcela.nombre_parcela}
            </div>
            <input type="text" id="coord-${index}" data-coord='${parcela.coordP}'>
            <div class="parcel-details" id="parcela-details-${index}">${parcela.ocupada ? 'Ocupada' : 'Disponible'}</div>
        `;

        const input = parcelInfo.querySelector(`#coord-${index}`);
        input.style.display = "none";
        // Asignar el evento onchange desde JavaScript
        const checkbox = parcelInfo.querySelector(`#parcela-${index}`);
        checkbox.onchange = () => toggleParcela(index, zona, checkbox, input);

        parcelItem.appendChild(parcelInfo);
        parcelasList.appendChild(parcelItem);
    });

    return parcelasList;
}

function toggleParcela(index, zona, checkbox, input) {
    let parcelaInput = JSON.parse(input.dataset.coord);
    const parcelaDetails = document.getElementById(`parcela-details-${index}`);

    if (checkbox.checked) {
        parcelaDetails.textContent = 'Ocupada';
        // Mostrar la parcela en el mapa
        mostrarParcelaEnMapa(parcelaInput, index);
    } else {
        parcelaDetails.textContent = 'Disponible';
        // Ocultar la parcela del mapa
        ocultarParcelaDelMapa(index);
    }
    actualizarParcelasJson(zona);
}

function mostrarParcelaEnMapa(parcelaInput, index) {
    console.log("Coordenadas de la parcela seleccionada: ", parcelaInput);

    if (parcelaInput && parcelaInput.length > 0) {
        const parcelaFeature = {
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: parcelaInput
            }
        };

        const layerId = `parcela-${index}`;
        const outlineLayerId = `parcela-outline-${index}`;

        console.log(`Agregando capa de parcela con ID: ${layerId}`, parcelaFeature);

        if (!map.getSource(layerId)) {
            console.log(`Añadiendo nueva fuente y capas para ${layerId}`);
            map.addSource(layerId, {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [parcelaFeature]
                }
            });

            map.addLayer({
                id: layerId,
                type: 'fill',
                source: layerId,
                layout: {},
                paint: {
                    'fill-color': '#FFD700',
                    'fill-opacity': 0.5
                }
            });

            map.addLayer({
                id: outlineLayerId,
                type: 'line',
                source: layerId,
                layout: {},
                paint: {
                    'line-color': '#FFD700',
                    'line-width': 2
                }
            });
        } else {
            console.log(`Actualizando datos de la fuente para ${layerId}`);
            map.getSource(layerId).setData({
                type: 'FeatureCollection',
                features: [parcelaFeature]
            });
        }
    } else {
        console.error(`No se encontraron coordenadas válidas para la parcela ${index}.`);
    }
}

function ocultarParcelaDelMapa(index) {
    const layerId = `parcela-${index}`;
    const outlineLayerId = `parcela-outline-${index}`;

    if (map.getLayer(outlineLayerId)) {
        map.removeLayer(outlineLayerId);
    }
    if (map.getLayer(layerId)) {
        map.removeLayer(layerId);
    }
    if (map.getSource(layerId)) {
        map.removeSource(layerId);
    }
}

function actualizarParcelasJson(zona) {
    const listaParcelas = [];
    const lista = document.getElementById('lista_zonas');
    lista.querySelectorAll('.parcel-list-item').forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        const input = item.querySelector('input[type="text"]');
        const nombre = item.querySelector('.parcel-status').innerText.trim();
        const coord = JSON.parse(input.dataset.coord);

        listaParcelas.push({
            nombre_parcela: nombre,
            ocupada: checkbox.checked,
            coordP: JSON.stringify(coord),
        });
    });


    document.getElementById('nombre_zona').value = zona.nombre;
    document.getElementById('id_zona').value = zona.document_id;
    document.getElementById('coordenadas_zona').value = zona.coordenadas_area;
    document.getElementById('lista_parcelas').value = JSON.stringify(listaParcelas);  // Almacena como string
    console.log(document.getElementById('nombre_zona').value, document.getElementById('id_zona').value, document.getElementById('coordenadas_zona').value, document.getElementById('lista_parcelas').value);
}

document.getElementById('btn-guardar').addEventListener('click', function () {
    document.getElementById('bitacora-form').submit();
});