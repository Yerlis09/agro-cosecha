const modalZona = document.getElementById("modalRegistrarDetalleZona"),
    myModalRegistrar = document.getElementById("myModalRegistrar"),
    btn_cancelar = document.getElementById("btn-cancelar"),
    coordInput = document.getElementById('registro_ubicacion'),
    numeroPInput = document.getElementById('registro_n_puntos'),
    numeroPAdd = document.getElementById('n_puntos'),
    ubicAdd = document.getElementById('ubicacion'),
    errorModal = document.getElementById("errorModal"),
    btn_error_cerrarM = document.getElementById("btn-error-cerrar"),
    btn_x = document.getElementById("btn-x"),
    zonaFormRegister = document.getElementById("area-form-register"), // Asegúrate de usar el ID correcto
    successModal = document.getElementById('successModalPar'),
    modalOkBtn = document.getElementById('btn-success-cerrar'),
    deleteButtons = document.querySelectorAll('.delete-btn');

// Obtener el token CSRF del meta tag
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


if (deleteButtons.length != 0) {
    const confirmDeleteModal = document.getElementById('confirmDeleteModal');
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const cancelButton = document.getElementById('cancelButton');
    const closeButton = document.querySelector('.close-button');
    let formToSubmit;

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            formToSubmit = button.closest('form');
            confirmDeleteModal.style.display = 'block';
        });
    });

    confirmDeleteButton.addEventListener('click', function () {
        if (formToSubmit) {
            formToSubmit.submit();
        }
    });

    cancelButton.addEventListener('click', function () {
        confirmDeleteModal.style.display = 'none';
    });

    closeButton.addEventListener('click', function () {
        confirmDeleteModal.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target == confirmDeleteModal) {
            confirmDeleteModal.style.display = 'none';
        }
    });
}

if (zonaFormRegister) {
    zonaFormRegister.addEventListener('submit', function (event) {
        event.preventDefault(); // Evitar la recarga de la página

        const formData = new FormData(zonaFormRegister);

        fetch(zonaFormRegister.action, {
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
            window.location.href = "/zona/mostrar_registros_zona"; // Redirige a la vista de la zona creada
        }, { once: true });
    });
}

function isAreaDelimitada() {
    const coordenadas = coordInput.value;
    return coordenadas !== '';
}

if (modalZona && myModalRegistrar) {
    modalZona.addEventListener("click", function () {
        if (isAreaDelimitada()) {
            myModalRegistrar.style.display = "block";
            myModalRegistrar.classList.add("show");
            ubicAdd.value = coordInput.value;
            numeroPAdd.value = numeroPInput.value;
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
    if (event.target === errorModal) {
        errorModal.style.display = "none";
    }
}

let map;
let draw;

function inicializarMapa() {
    if (!map) { // Asegúrate de que el mapa no se inicializa múltiples veces
        map = new maplibregl.Map({
            container: 'map',
            style: 'https://api.maptiler.com/maps/hybrid/style.json?key=A1mAVA0b8Lsf3DtgWE85',
            center: [-75.4794, 10.3910],
            zoom: 12
        });

        draw = new MapboxDraw({
            displayControlsDefault: false,
            controls: {
                polygon: true,
                trash: true
            },
            defaultMode: 'draw_polygon',
            styles: [
                {
                    'id': 'gl-draw-polygon-stroke-active',
                    'type': 'line',
                    'filter': ['all', ['==', '$type', 'Polygon'], ['!=', 'mode', 'static']],
                    'paint': {
                        'line-color': '#D20C0C',
                        'line-width': 2
                    }
                },
                {
                    'id': 'gl-draw-polygon-stroke-casing',
                    'type': 'line',
                    'filter': ['all', ['==', '$type', 'Polygon'], ['!=', 'mode', 'static']],
                    'paint': {
                        'line-color': '#D20C0C',
                        'line-width': 2
                    }
                },
                {
                    'id': 'gl-draw-polygon-and-line-vertex-halo-active',
                    'type': 'circle',
                    'filter': ['all', ['==', '$type', 'Point'], ['==', 'meta', 'vertex'], ['!=', 'mode', 'static']],
                    'paint': {
                        'circle-radius': 5,
                        'circle-color': '#FFF'
                    }
                },
                {
                    'id': 'gl-draw-polygon-and-line-vertex-active',
                    'type': 'circle',
                    'filter': ['all', ['==', '$type', 'Point'], ['==', 'meta', 'vertex'], ['!=', 'mode', 'static']],
                    'paint': {
                        'circle-radius': 3,
                        'circle-color': '#D20C0C',
                    }
                }
            ]
        });

        map.addControl(draw, 'top-left');

        map.on('draw.create', actualizarCoordenadaPoligono);
        map.on('draw.update', actualizarCoordenadaPoligono);
        map.on('draw.delete', limpiarCoordenadasPoligono);

        // Manejar el clic del botón para limpiar la zona
        document.getElementById('clear-zone-btn').addEventListener('click', function () {
            draw.deleteAll();
            draw.changeMode('draw_polygon');
            limpiarFormulario();
            //parcelas = [];
            console.log('Zona y parcelas limpiadas');
        });
    }
}

function actualizarCoordenadaPoligono(e) {
    const data = draw.getAll();
    if (data.features.length > 0) {
        const coordinates = data.features[0].geometry.coordinates[0];
        console.log('Coordenadas del polígono:', coordinates);
        mostrarCoordenadasEnFormulario(coordinates);
        actualizarNumeroDePuntos(coordinates);
    } else {
        console.log('No hay polígonos dibujados');
        actualizarNumeroDePuntos([]);
    }
}

function limpiarCoordenadasPoligono(e) {
    console.log('Polígono eliminado');
    limpiarFormulario();
}

function mostrarCoordenadasEnFormulario(coordinates) {
    const coordenadasInput = document.getElementById('registro_ubicacion');
    coordenadasInput.value = JSON.stringify(coordinates);
}

function actualizarNumeroDePuntos(coordinates) {
    const numeroPuntosInput = document.getElementById('registro_n_puntos');
    numeroPuntosInput.value = coordinates.length;
}

function limpiarFormulario() {
    const coordenadasInput = document.getElementById('registro_ubicacion');
    coordenadasInput.value = '';
    const numeroPuntosInput = document.getElementById('registro_n_puntos');
    numeroPuntosInput.value = '';
}


window.onload = inicializarMapa;
