const modalZona = document.getElementById("modalRegistrarParcela"),
    myModalRegistrar = document.getElementById("myModalRegistrar"),
    btn_cancelar = document.getElementById("btn-cancelar"),
    coordP = document.getElementById("coordP"),
    coordParcela = document.getElementById("coordParcela"),
    errorModal = document.getElementById("errorModal"),
    btn_error_cerrarM = document.getElementById("btn-error-cerrar"),
    btn_x = document.getElementById("btn-x"),
    parcelaFormRegister = document.getElementById("parcela-form-register"), // Asegúrate de usar el ID correcto
    successModal = document.getElementById('successModalPar'),
    modalOkBtn = document.getElementById('btn-success-cerrar');

    const zonaId = document.getElementById('zonaId').value;

let map;
let parcelaDraw;
let selectedParcelaId = null;

if (parcelaFormRegister) {
    parcelaFormRegister.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(parcelaFormRegister);

        fetch(parcelaFormRegister.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrf_token]').value
            }
        }).then(response => response.json())
            .then(data => {
                if (data.success) {
                    myModalRegistrar.style.display = 'none';
                    successModal.style.display = 'block';
                } else {
                    alert(`Error: ${data.error}`);
                    console.error('Error:', data.error);
                }
            }).catch(error => {
                alert(`Error: ${error.message}`);
                console.error('Error:', error);
            });

        modalOkBtn.addEventListener('click', function () {
            successModal.style.display = 'none';
            window.location.href = `/zona/ver/${zonaId}`;
}, { once: true });
    });
}

function isAreaDelimitada() {
    const coordenadas = coordP.value;
    return coordenadas !== '';
}

if (modalZona && myModalRegistrar) {
    modalZona.addEventListener("click", function () {
        if (isAreaDelimitada()) {
            myModalRegistrar.style.display = "block";
            myModalRegistrar.classList.add("show");
            coordParcela.value = coordP.value;
        } else {
            errorModal.style.display = "block"; // Mostrar el modal de error
        }
    });
}

if (btn_cancelar) {
    btn_cancelar.addEventListener("click", e => {
        myModalRegistrar.style.display = "none";
        myModalRegistrar.classList.remove("show");
    });
}

if (btn_error_cerrarM) {
    btn_error_cerrarM.addEventListener("click", e => {
        errorModal.style.display = "none";
    });
}

if (btn_x) {
    btn_x.addEventListener("click", e => {
        errorModal.style.display = "none";
    });
}

window.onclick = function (event) {
    if (event.target === myModalRegistrar) {
        myModalRegistrar.style.display = "none";
        myModalRegistrar.classList.remove("show");
    }
}


function inicializarMapa() {
    if (!map) {
        map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/hybrid/style.json?key=A1mAVA0b8Lsf3DtgWE85',
            center: [-75.4794, 10.3910],
            zoom: 12
        });

        // Control de dibujo para parcelas
        parcelaDraw = new MapboxDraw({
            displayControlsDefault: false,
            controls: {
                polygon: true,
                trash: true
            },
            defaultMode: 'draw_polygon',
            styles: [
                {
                    'id': 'gl-draw-polygon-stroke-active-parcela',
                    'type': 'line',
                    'filter': ['all', ['==', '$type', 'Polygon'], ['!=', 'mode', 'static']],
                    'paint': {
                        'line-color': '#FFD700',
                        'line-width': 2
                    }
                },
                {
                    'id': 'gl-draw-polygon-fill-parcela',
                    'type': 'fill',
                    'filter': ['all', ['==', '$type', 'Polygon'], ['!=', 'mode', 'static']],
                    'paint': {
                        'fill-color': '#FFD700',
                        'fill-opacity': 0.5
                    }
                },
                {
                    'id': 'gl-draw-polygon-and-line-vertex-halo-active-parcela',
                    'type': 'circle',
                    'filter': ['all', ['==', '$type', 'Point'], ['==', 'meta', 'vertex'], ['!=', 'mode', 'static']],
                    'paint': {
                        'circle-radius': 5,
                        'circle-color': '#FFF'
                    }
                },
                {
                    'id': 'gl-draw-polygon-and-line-vertex-active-parcela',
                    'type': 'circle',
                    'filter': ['all', ['==', '$type', 'Point'], ['==', 'meta', 'vertex'], ['!=', 'mode', 'static']],
                    'paint': {
                        'circle-radius': 3,
                        'circle-color': '#FFD700',
                    }
                }
            ]
        });

        map.addControl(parcelaDraw, 'top-left');

        map.on('draw.create', actualizarCoordenadaParcela);
        map.on('draw.update', actualizarCoordenadaParcela);
        map.on('draw.delete', limpiarCoordenadasParcela);

        document.getElementById('clear-zone-btn').addEventListener('click', function () {
            if (selectedParcelaId) {
                console.log('Intentando eliminar parcela con ID:', selectedParcelaId);
                parcelaDraw.delete(selectedParcelaId);
                const deletedFeature = parcelaDraw.get(selectedParcelaId);
                if (!deletedFeature) {
                    console.log('Parcela eliminada correctamente del mapa. id:', selectedParcelaId);
                } else {
                    console.log('Parcela no se pudo eliminar del mapa.');
                }
                limpiarFormulario();
                selectedParcelaId = null;
                parcelaDraw.changeMode('draw_polygon');
            } else {
                console.log('No hay parcela seleccionada para limpiar');
            }
        });


        // Cargar el área principal desde el input
        mostrarZonaGuardada();
    }
}

function actualizarCoordenadaParcela(e) {
    const data = parcelaDraw.getAll();
    if (data.features.length > 0) {
        const ultimaParcela = data.features[0]; // Obtener la última parcela agregada que se encuentra en la posición 0
        const coordinates = ultimaParcela.geometry.coordinates;
        const ultimaParcelaId = data.features.find(feature => feature.id === e.features[0].id); // Encontrar la parcela agregada o actualizada

        selectedParcelaId = ultimaParcelaId.id; // Guardar el ID de la parcela seleccionada
        mostrarCoordenadasEnParcela(coordinates);
        console.log('Coordenadas de la parcela:', coordinates);
        console.log('Ultima parcela:', selectedParcelaId);
    } else {
        console.log('No hay parcelas dibujadas');
        selectedParcelaId = null; // Asegurarse de que no quede un ID de parcela obsoleto
    }
}

function mostrarCoordenadasEnParcela(coordinates) {
    console.log("coordenadas actual", coordinates)
    const coordenadasInput = document.getElementById('coordP');
    coordenadasInput.value = JSON.stringify(coordinates);
}

function limpiarCoordenadasParcela(e) {
    limpiarFormulario();
    console.log('Parcela eliminada');
}

function mostrarZonaGuardada() {
    const coordInput = document.getElementById('ubicacion');

    if (coordInput && coordInput.value) {
        const coordinates = JSON.parse(coordInput.value);
        console.log("Coordenadas del área:", coordinates);

        if (coordinates && coordinates.length > 0) {
            const areaFeature = {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: [coordinates]
                }
            };

            // Añadir el área como una capa en el mapa, no modificable
            map.on('load', () => {
                map.addLayer({
                    id: 'area',
                    type: 'fill',
                    source: {
                        type: 'geojson',
                        data: {
                            type: 'FeatureCollection',
                            features: [areaFeature]
                        }
                    },
                    layout: {},
                    paint: {
                        'fill-color': '#888888',
                        'fill-opacity': 0.4
                    }
                });

                map.addLayer({
                    id: 'area-outline',
                    type: 'line',
                    source: {
                        type: 'geojson',
                        data: {
                            type: 'FeatureCollection',
                            features: [areaFeature]
                        }
                    },
                    layout: {},
                    paint: {
                        'line-color': '#000000',
                        'line-width': 2
                    }
                });

                map.flyTo({ center: coordinates[0], zoom: 12 }); // Ajustar la vista del mapa a la zona
            });

            // Cargar las parcelas guardadas
            cargarParcelasGuardadas();
        } else {
            console.error('No se encontraron coordenadas válidas en el input.');
        }
    } else {
        console.error('No se encontraron coordenadas en el input.');
    }

}

function cargarParcelasGuardadas() {
    const arrayPs = document.getElementById("zone-data");
    let parcelas = JSON.parse(arrayPs.getAttribute("data-parcelas"));
    console.log(parcelas);

    if (parcelas.length > 0) {
        parcelas.forEach(parcela => {
            let coordP = JSON.parse(parcela.coordP);
            console.log(coordP);

            parcelaDraw.add({
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: coordP
                }
            });
        });
    } else {
        console.log("No hay parcelas disponibles");
    }
}

function limpiarFormulario() {
    coordP.value = '';
    coordParcela.value = '';
}

window.onload = inicializarMapa;
