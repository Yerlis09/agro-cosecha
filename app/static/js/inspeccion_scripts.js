document.addEventListener('DOMContentLoaded', (event) => {
    const inspeccionCampoId = document.getElementById('document_id').value;
    const mapDiv = document.getElementById('mapDiv');

    // Hacer todos los inputs de solo lectura
    const inputs = document.querySelectorAll('#inspeccion-campo-form input');
    inputs.forEach(input => {
        input.readOnly = true;
    });

    cargarZonaYParcelasGuardadas(mapDiv);
    obtenerInspecciones(inspeccionCampoId);
});

const modalInspeccion = document.getElementById("btn-inspeccion"),
    myModalRegistrar = document.getElementById("myModalInspeccion"),
    btn_cancelar = document.getElementById("btn-cancelar"),
    errorModal = document.getElementById("errorModal"),
    btn_error_cerrar = document.getElementById("btn-error-cerrar"),
    layersId = document.getElementById('tbxListLayerId'),
    outLayersId = document.getElementById('tbxListOutLayerId'),
    btn_guardar = document.getElementById('btn-guardar');

let parcelasSeleccionadas = new Set();
let listaDeOutLayerId = new Set();
let map;

if (btn_guardar) {
    btn_guardar.addEventListener('click', function () {
        document.getElementById('inspeccion-form').submit();
    });
}

// Mostrar modal de registrar inspección o modal de error
if (modalInspeccion) {
    modalInspeccion.addEventListener("click", function (e) {
        e.preventDefault();
        if (isParcelaSeleccionada()) {
            const identificadorUnico = generarIdentificadorUnico();
            document.getElementById('inspeccion').value = identificadorUnico;
            layersId.value = JSON.stringify(Array.from(parcelasSeleccionadas));
            outLayersId.value = JSON.stringify(Array.from(listaDeOutLayerId));
            $('#myModalInspeccion').modal('show');
        } else {
            $('#errorModal').modal('show');
        }
    });
}

// Cerrar modal de error al hacer clic en el botón de cerrar
if (btn_error_cerrar) {
    btn_error_cerrar.addEventListener("click", function (e) {
        $('#errorModal').modal('hide');
    });
}

// Manejar click en el botón cancelar del modal de registrar
if (btn_cancelar) {
    btn_cancelar.addEventListener("click", e => {
        myModalRegistrar.style.display = "none";
        myModalRegistrar.classList.remove("show");
    });
}

// Cerrar modal cuando se hace click fuera del modal
window.addEventListener("click", e => {
    if (e.target === myModalRegistrar) {
        myModalRegistrar.style.display = "none";
        myModalRegistrar.classList.remove("show");
    }
});

// Filtrar Bitácora
function filtrarBitacora(inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const lista = document.getElementById(listaId);

    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar llamada para obtener los clientes filtrados
    fetch("/inspeccion_campo/filtrar_bitacoras", {
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
        const resultados = document.getElementById('resultados_dat_bitacora');
        resultados.innerHTML = "";
        if (input.value != "") {
            if (data.bitacoras.length > 0) {
                resultados.style.display = "block";  // Mostrar el div
                data.bitacoras.forEach(bitacora => {
                    const div = document.createElement("div");
                    div.classList.add("list-group-item");
                    div.textContent = `${bitacora.nombre}`;
                    div.onclick = () => seleccionarBitacora(bitacora, inputId);
                    resultados.appendChild(div);
                });
            }
        }
    })
    .catch(error => {
        console.error("Error al obtener bitacoras:", error);
    });
}

function cargarZonaYParcelasGuardadas(mapDiv) {
    const idCuaderno = document.getElementById('id_cuaderno').value;
    if (!idCuaderno) {
        console.error('ID del cuaderno no encontrado.');
        return;
    }

    fetch(`/inspeccion_campo/obtener_zona_por_bitacora/${idCuaderno}`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
            return;
        }

        const zona = {
            nombre: data.bitacoras.nombre_zona,
            coordenadas_area: data.bitacoras.coordenadas_zona,
            lista_parcelas: data.bitacoras.lista_parcelas
        };

        inicializarMapa(null, zona, mapDiv);
    })
    .catch(error => {
        console.error('Error al obtener la zona:', error);
    });
}

function seleccionarBitacora(bitacora, inputId) {
    const input = document.getElementById(inputId);
    const inputIdBit = document.getElementById('id_cuaderno');
    if (!input) {
        console.error(`Elemento con ID ${inputId} no encontrado.`);
        return;
    }
    input.value = bitacora.nombre;
    input.readOnly = true;

    // Eliminar botón de eliminar anterior, si existe
    const inputContainer = input.parentNode;
    const btnEliminarPrev = inputContainer.querySelector('.btn-clear-vuelo');
    if (btnEliminarPrev) {
        btnEliminarPrev.remove();
    }

    const btnEliminar = document.createElement("button");
    btnEliminar.classList.add("btn-clear-vuelo");
    btnEliminar.innerHTML = "<i class='bx bx-trash-alt'></i>";
    btnEliminar.onclick = () => eliminarBitacora(inputId);
    inputContainer.appendChild(btnEliminar);

    // Limpiar el campo de búsqueda y los resultados
    const resultados = document.getElementById('resultados_dat_bitacora');
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
    inputIdBit.value = bitacora.document_id;
}

function eliminarBitacora(inputId) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.error(`Elemento con ID ${inputId} no encontrado.`);
        return;
    }
    input.value = "";
    duracionInput.value = "";
    input.readOnly = false;

    // Eliminar botón de eliminar
    const btnEliminar = input.parentNode.querySelector('.btn-clear-inspeccion');
    if (btnEliminar) {
        btnEliminar.remove();
    }
}

function inicializarMapa(bitacora, zona, mapDiv) {
    let coordinatesZona = null;
    if (bitacora != null) {
        coordinatesZona = bitacora.coordenadas_zona;
    } else {
        coordinatesZona = zona.coordenadas_area;
        mapDiv.style.display = "block";
    }

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
                mostrarZonaGuardada(coordinatesZona, bitacora, zona);
            } else {
                map.once('styledata', () => {
                    mostrarZonaGuardada(coordinatesZona, bitacora, zona);
                });
            }
        });

        map.on('error', (e) => {
            console.error("Error al cargar el mapa: ", e);
        });
    } else {
        // Si el mapa ya está inicializado, simplemente muestra la nueva zona
        mostrarZonaGuardada(coordinatesZona, bitacora, zona);
        map.resize();
    }
}

function mostrarZonaGuardada(coordinatesZona, bitacora, zona) {
    const coordinates = JSON.parse(coordinatesZona);

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

        map.flyTo({ center: coordinates[0], zoom: 15 }); // Ajustar la vista del mapa a la zona
        mostrarParcelasEnMapa(bitacora, zona);
    } else {
        console.error('No se encontraron coordenadas válidas en la zona.');
    }
}

function transformarListaParcelas(parcelasJson) {
    // Reemplazar True y False por true y false
    parcelasJson = parcelasJson.replace(/True/g, 'true').replace(/False/g, 'false');

    try {
        parcelasJson = parcelasJson.replace(/'/g, '"'); // Reemplazar comillas simples por dobles
        const tempParcelasData = JSON.parse(parcelasJson);

        // Verificar y analizar cada coordP individualmente
        const parcelasData = tempParcelasData.map(parcela => {
            if (typeof parcela.coordP === 'string') {
                try {
                    parcela.coordP = JSON.parse(parcela.coordP);
                } catch (e) {
                    console.error("Error al parsear coordP en parcela:", e);
                }
            }
            return parcela;
        });

        return parcelasData;
    } catch (e) {
        console.error("Error al parsear JSON de parcelas:", e);
        return [];
    }
}

function mostrarParcelasEnMapa(bitacora, zona) {
    let listaParcelasJson = null;
    if (bitacora != null) {
        listaParcelasJson = transformarListaParcelas(bitacora.lista_parcelas);
    } else {
        listaParcelasJson = transformarListaParcelas(zona.lista_parcelas);
    }

    listaParcelasJson.forEach((parcela, index) => {
        if (!parcela.ocupada) {
            return; // Saltar parcelas no ocupadas
        }

        try {
            const coordP = typeof parcela.coordP === 'string' ? JSON.parse(parcela.coordP) : parcela.coordP;
            const parcelaFeature = {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: coordP
                }
            };

            const layerId = `parcela-${index}`;
            const outlineLayerId = `parcela-outline-${index}`;

            if (!map.getSource(layerId)) {
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

                map.on('click', layerId, (e) => {
                    toggleParcelaSeleccionada(layerId, outlineLayerId);
                });
            } else {
                map.getSource(layerId).setData({
                    type: 'FeatureCollection',
                    features: [parcelaFeature]
                });
            }
        } catch (e) {
            console.error("Error al parsear coordP en parcela:", e);
        }
    });
}

// Función para alternar la selección de una parcela en el mapa
function toggleParcelaSeleccionada(layerId, outlineLayerId) {
    const currentColor = map.getPaintProperty(layerId, 'fill-color');
    const newColor = currentColor === '#FFD700' ? 'rgba(0, 0, 255, 0.3)' : '#FFD700'; // Cambiar entre dorado y azul claro
    const newOutlineColor = currentColor === '#FFD700' ? 'rgba(0, 0, 255, 0.5)' : '#FFD700'; // Cambiar entre dorado y azul claro

    map.setPaintProperty(layerId, 'fill-color', newColor);
    map.setPaintProperty(outlineLayerId, 'line-color', newOutlineColor);

    // Actualizar el estado de selección en la estructura de datos
    if (newColor === 'rgba(0, 0, 255, 0.3)') {
        parcelasSeleccionadas.add(layerId);
        listaDeOutLayerId.add(outlineLayerId);
    } else {
        parcelasSeleccionadas.delete(layerId);
        listaDeOutLayerId.delete(outlineLayerId);
    }
}

// Verificar si hay una parcela seleccionada
function isParcelaSeleccionada() {
    return parcelasSeleccionadas.size > 0;
}

function generarIdentificadorUnico() {
    let inspeccionCounter = parseInt(localStorage.getItem('inspeccionCounter')) || 0;
    inspeccionCounter += 1;
    localStorage.setItem('inspeccionCounter', inspeccionCounter);
    return `Inspección nro. ${inspeccionCounter}`;
}

function obtenerInspecciones(inspeccionCampoId) {
    fetch(`/inspeccion_campo/obtener_inspecciones/${inspeccionCampoId}`)
    .then(response => response.json())
    .then(data => {
        if (data.inspecciones) {
            mostrarInspecciones(data.inspecciones, inspeccionCampoId);
            // Guardar las inspecciones realizadas y estimadas en el local storage para usarlas en el evento click
            localStorage.setItem('inspecciones_realizadas', data.inspecciones_realizadas);
            localStorage.setItem('inspecciones_estimadas', data.inspecciones_estimadas);
        } else {
            console.error('Error al obtener inspecciones:', data.error);
        }
    })
    .catch(error => {
        console.error('Error al obtener inspecciones:', error);
    });
}

function mostrarInspecciones(inspecciones, inspeccionCampoId) {
    const listaInspecciones = document.getElementById('lista_inspecciones');
    listaInspecciones.innerHTML = '';  // Limpiar la lista actual

    inspecciones.forEach((inspeccion, index) => {
        const inspeccionItem = document.createElement('li');
        inspeccionItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');

        inspeccionItem.innerHTML = `
            <div>
                <i class='bx bxs-inspeccion-alt'></i> Inspección #${index + 1}<br>
                ${inspeccion.fecha_inicio} ${inspeccion.hora_inicio}
            </div>
            <button class="btn btn-success" id="btn-ver-inspeccion-${index}" data-index="${index}">Ver</button>
        `;

        listaInspecciones.appendChild(inspeccionItem);
    });

    // Agregar evento a cada botón de ver inspección
    inspecciones.forEach((inspeccion, index) => {
        const btnVerInspeccion = document.getElementById(`btn-ver-inspeccion-${index}`);
        btnVerInspeccion.addEventListener('click', (e) => {
            e.preventDefault();  // Evitar que se envíe el formulario
            abrirModalEditarInspeccion(inspeccion, inspeccionCampoId);
        });
    });
}

function abrirModalEditarInspeccion(inspeccion, inspeccionCampoId) {
    // Cargar la información de la inspección en el formulario
    document.getElementById('inspeccion_actualizar').value = inspeccion.inspeccion;
    document.getElementById('fecha_inicio_actualizar').value = inspeccion.fecha_inicio;
    document.getElementById('hora_inicio_actualizar').value = inspeccion.hora_inicio;
    document.getElementById('hora_fin_actualizar').value = inspeccion.hora_fin;
    document.getElementById('observ_actualizar').value = inspeccion.observ;
    document.getElementById('listLayerId_actualizar').value = inspeccion.listLayerId;
    document.getElementById('listOutLayerId_actualizar').value = inspeccion.listOutLayerId;

    // Establecer la URL correcta en el formulario
    const form = document.getElementById('formActualizarInspeccion');
    form.action = `/inspeccion_campo/actualizar_inspeccion/${inspeccionCampoId}/${inspeccion.id}`;

    verParcelas(inspeccion);

    // Mostrar el modal
    $('#myModalActualizarInspeccion').modal('show');
}

function verParcelas(inspeccion) {
    // Primero, restaurar todas las parcelas a su color original
    const allParcelas = Array.from(parcelasSeleccionadas);
    allParcelas.forEach(layerId => {
        const outlineLayerId = `parcela-outline-${layerId.split('-')[1]}`;
        map.setPaintProperty(layerId, 'fill-color', '#FFD700');  // Color dorado original
        map.setPaintProperty(outlineLayerId, 'line-color', '#FFD700');  // Color dorado original
    });

    // Limpiar la lista de parcelas seleccionadas
    parcelasSeleccionadas.clear();
    listaDeOutLayerId.clear();

    // Luego, resaltar solo las parcelas específicas de la inspección
    const parcelas = JSON.parse(inspeccion.listLayerId);
    const outLayers = JSON.parse(inspeccion.listOutLayerId);

    parcelas.forEach((layerId, index) => {
        const outlineLayerId = outLayers[index];
        map.setPaintProperty(layerId, 'fill-color', 'rgba(0, 0, 255, 0.3)');  // Azul claro
        map.setPaintProperty(outlineLayerId, 'line-color', 'rgba(0, 0, 255, 0.5)');  // Azul claro

        // Agregar las parcelas específicas de la inspección a la lista de parcelas seleccionadas
        parcelasSeleccionadas.add(layerId);
        listaDeOutLayerId.add(outlineLayerId);
    });
}


