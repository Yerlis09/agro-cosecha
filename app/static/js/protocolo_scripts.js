// Mapeo de periodicidades
const periodicidades = {
    'D1': 'Diario',
    'Q2': 'Quincenal',
    'M3': 'Mensual',
    'T4': 'Trimestral',
    'S5': 'Semestral'
};


const inforObtDesdeSelect = document.getElementById('id_infor_obt_desde');
const vuelosSection = document.querySelector('.vuelos-card-body');
const detectoresSection = document.querySelector('.detectores-card-body');
const inspeccionesSection = document.querySelector('.inspecciones-card-body');
const btn_guardar = document.getElementById('btn-guardar');
const idHerra = document.getElementById('buscar_herramienta');
const selectAltNoQuimica = document.getElementById('alt_no_quimica');
const descAltQuimicaSection = document.getElementById('descAltQuimicaSection');
const listaHerramientasInput = document.getElementById('lista_herra_select');
const listaVuelosInput = document.getElementById('lista_vuelos_select');
const listaDetectoresInput = document.getElementById('lista_detectores_select');
const listaInspeccionesInput = document.getElementById('lista_inspecc_select');
const inputDescAltQuimica = document.getElementById('descr_alt_no_quimica');


let cuadernoId = document.getElementById('id_cuaderno').value;

if (selectAltNoQuimica) {
    selectAltNoQuimica.addEventListener('change', function () {
        if (this.value === 'A1') {
            descAltQuimicaSection.style.display = 'block';
        } else {
            descAltQuimicaSection.style.display = 'none';
            inputDescAltQuimica.value = "";
        }
    });
}

/*if (cuadernoId) {
    obtenerVuelos(cuadernoId);
    obtenerSensores(cuadernoId);
    obtenerInspecciones(cuadernoId);
    obtenerHerramientas(cuadernoId);
}*/

// Inicialmente ocultar todas las secciones
function esPaginaEditar() {
    // Verifica si hay un campo específico presente solo en la página de edición
    return document.getElementById('es_editar') !== null;
}

// Inicialmente ocultar todas las secciones si no estamos en la página de edición
if (!esPaginaEditar()) {
    ocultarSecciones();
}

// Evento para cambiar la visibilidad de las secciones según la selección
if (inforObtDesdeSelect) {
    inforObtDesdeSelect.addEventListener('change', (e) => {
        const selectedValue = e.target.value;
        if (selectedValue === 'V1') {
            mostrarSeccion('vuelos');
        } else if (selectedValue === 'D2') {
            mostrarSeccion('detectores');
        } else if (selectedValue === 'I3') {
            mostrarSeccion('inspecciones');
        } else {
            ocultarSecciones();
        }
    });
}

function mostrarSeccion(seccion) {
    limpiarTablas();
    const secciones = ['vuelos', 'detectores', 'inspecciones'];
    secciones.forEach(sec => {
        const elemento = document.querySelector(`.${sec}-card-body`);
        if (sec === seccion) {
            elemento.style.display = 'block';
        } else {
            elemento.style.display = 'none';
        }
    });
}

function ocultarSecciones() {
    idHerra.readOnly = true;
    inforObtDesdeSelect.disabled = true;
    const secciones = ['vuelos', 'detectores', 'inspecciones'];
    secciones.forEach(sec => {
        const elemento = document.querySelector(`.${sec}-card-body`);
        elemento.style.display = 'none';
    });
}

function limpiarTablas() {
    const idsTablas = ['lista_vuelos', 'lista_detectores', 'lista_inspecciones'];
    const idsInputs = ['buscar_vuelo', 'buscar_sensor', 'buscar_inspeccion'];
    const idsResultados = ['resultados_vuelos', 'resultados_sensores', 'resultados_inspecciones'];

    idsTablas.forEach(id => {
        const tabla = document.getElementById(id);
        if (tabla) {
            tabla.innerHTML = '';
        }
    });

    idsInputs.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            input.value = '';
        }
    });

    idsResultados.forEach(id => {
        const resultados = document.getElementById(id);
        if (resultados) {
            resultados.innerHTML = '';
            resultados.style.display = 'none';
        }
    });
}

if (btn_guardar) {
    btn_guardar.addEventListener('click', function () {
        const listaHerramientas = getListaHerramientas();
        const listaVuelos = getListaVuelos();
        const listaDetectores = getListaDetectores();
        const listaInspecciones = getListaInspecciones();


        listaHerramientasInput.value = JSON.stringify(listaHerramientas);
        listaVuelosInput.value = JSON.stringify(listaVuelos);
        listaDetectoresInput.value = JSON.stringify(listaDetectores);
        listaInspeccionesInput.value = JSON.stringify(listaInspecciones);
        document.getElementById('bitacora-form').submit();
    });
}

function getListaHerramientas() {
    const tabla = document.getElementById('lista_herramientas');
    const filas = tabla.getElementsByTagName('tr');
    const listaHerramientas = [];

    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas.length > 0) {
            const herramienta = {
                nombre: celdas[1].innerText,
                funcionalidad: celdas[2].innerText
            };
            listaHerramientas.push(herramienta);
        }
    }
    return listaHerramientas.length > 0 ? listaHerramientas : [];
}

function getListaVuelos() {
    const tabla = document.getElementById('lista_vuelos');
    const filas = tabla.getElementsByTagName('tr');
    const listaVuelos = [];

    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas.length > 0) {
            const vuelo = {
                nombre: celdas[1].innerText,
                fecha: celdas[2].innerText,
                duracion: celdas[3].innerText,
                periocidad: celdas[4].innerText
            };
            listaVuelos.push(vuelo);
        }
    }
    return listaVuelos.length > 0 ? listaVuelos : [];
}

function getListaDetectores() {
    const tabla = document.getElementById('lista_detectores');
    const filas = tabla.getElementsByTagName('tr');
    const listaDetectores = [];

    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas.length > 0) {
            const detector = {
                nombre: celdas[1].innerText,
                fecha: celdas[2].innerText,
                duracion: celdas[3].innerText,
                periocidad: celdas[4].innerText
            };
            listaDetectores.push(detector);
        }
    }
    return listaDetectores.length > 0 ? listaDetectores : [];
}

function getListaInspecciones() {
    const tabla = document.getElementById('lista_inspecciones');
    const filas = tabla.getElementsByTagName('tr');
    const listaInspecciones = [];

    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas.length > 0) {
            const inspeccion = {
                nombre: celdas[1].innerText,
                fecha: celdas[2].innerText,
                duracion: celdas[3].innerText,
                periocidad: celdas[4].innerText
            };
            listaInspecciones.push(inspeccion);
        }
    }
    return listaInspecciones.length > 0 ? listaInspecciones : [];
}

// Filtrar Bitácora
function filtrarBitacora(inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();
    const lista = document.getElementById(listaId);

    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Realizar llamada para obtener los clientes filtrados
    fetch("/protocolo/filtrar_bitacoras", {
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

    // Permitir selección de registros asociados
    habilitarSeleccion();
}

function habilitarSeleccion() {
    idHerra.readOnly = false;
    inforObtDesdeSelect.disabled = false;

}

function deshabilitarSeleccion() {
    idHerra.readOnly = true;
    inforObtDesdeSelect.disabled = true;
}

function eliminarBitacora(inputId) {
    const input = document.getElementById(inputId);
    if (!input) {
        console.error(`Elemento con ID ${inputId} no encontrado.`);
        return;
    }
    input.value = "";
    input.readOnly = false;

    // Eliminar botón de eliminar
    const btnEliminar = input.parentNode.querySelector('.btn-clear-vuelo');
    if (btnEliminar) {
        btnEliminar.remove();
    }

    // Ocultar secciones y deshabilitar selección de registros asociados
    ocultarSecciones();
    deshabilitarSeleccion();
}

function obtenerVuelos1(cuadernoId) {
    fetch(`/protocolo/filtrar_planes_vuelo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: '' })
    })
        .then(response => response.json())
        .then(data => {
            if (data.planes_vuelo) {
                mostrarVuelos(data.planes_vuelo);
            } else {
                console.error('Error al obtener vuelos:', data.error);
            }
        })
        .catch(error => {
            console.error('Error al obtener vuelos:', error);
        });
}

function mostrarVuelos(vuelos) {
    const listaVuelos = document.getElementById('lista_vuelos');
    listaVuelos.innerHTML = '';  // Limpiar la lista actual

    vuelos.forEach((vuelo, index) => {
        const vueloItem = document.createElement('tr');

        vueloItem.innerHTML = `
            <td>${index + 1}</td>
            <td>${vuelo.codigo}</td>
            <td>${vuelo.fecha_inicio}</td>
            <td>${vuelo.fecha_fin}</td>
            <td>${vuelo.resultado}</td>
            <td><button type="button" class="btn btn-danger" id="btn-eliminar-vuelo-${index}"><i class='bx bx-trash-alt'></i></button></td>
        `;

        listaVuelos.appendChild(vueloItem);

        // Agregar evento al botón de eliminar vuelo
        const btnEliminarVuelo = document.getElementById(`btn-eliminar-vuelo-${index}`);
        btnEliminarVuelo.addEventListener('click', (e) => {
            e.preventDefault();  // Evitar que se envíe el formulario
            eliminarVuelo(index);
        });
    });
}

function eliminarVuelo(index) {
    const listaVuelos = document.getElementById('lista_vuelos');
    listaVuelos.deleteRow(index);
}

function obtenerSensores(cuadernoId) {
    fetch(`/protocolo/filtrar_detectores`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: '' })
    })
        .then(response => response.json())
        .then(data => {
            if (data.detectores) {
                mostrarSensores(data.detectores);
            } else {
                console.error('Error al obtener sensores:', data.error);
            }
        })
        .catch(error => {
            console.error('Error al obtener sensores:', error);
        });
}

function mostrarSensores(sensores) {
    const listaSensores = document.getElementById('lista_sensores');
    listaSensores.innerHTML = '';  // Limpiar la lista actual

    sensores.forEach((sensor, index) => {
        const sensorItem = document.createElement('tr');

        sensorItem.innerHTML = `
            <td>${index + 1}</td>
            <td>${sensor.codigo}</td>
            <td>${sensor.fecha_inicio}</td>
            <td>${sensor.hora_inicio}</td>
            <td>${sensor.hora_fin}</td>
            <td>${sensor.observacion}</td>
            <td><button type="button" class="btn btn-danger" id="btn-eliminar-sensor-${index}"><i class='bx bx-trash-alt'></i></button></td>
        `;

        listaSensores.appendChild(sensorItem);

        // Agregar evento al botón de eliminar sensor
        const btnEliminarSensor = document.getElementById(`btn-eliminar-sensor-${index}`);
        btnEliminarSensor.addEventListener('click', (e) => {
            e.preventDefault();  // Evitar que se envíe el formulario
            eliminarSensor(index);
        });
    });
}

function eliminarSensor(index) {
    const listaSensores = document.getElementById('lista_sensores');
    listaSensores.deleteRow(index);
}

function obtenerInspecciones(cuadernoId) {
    fetch(`/protocolo/filtrar_inspecciones_campo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: '' })
    })
        .then(response => response.json())
        .then(data => {
            if (data.inspecciones_campo) {
                mostrarInspecciones(data.inspecciones_campo);
            } else {
                console.error('Error al obtener inspecciones:', data.error);
            }
        })
        .catch(error => {
            console.error('Error al obtener inspecciones:', error);
        });
}

function mostrarInspecciones(inspecciones) {
    const listaInspecciones = document.getElementById('lista_inspecciones');
    listaInspecciones.innerHTML = '';  // Limpiar la lista actual

    inspecciones.forEach((inspeccion, index) => {
        const inspeccionItem = document.createElement('tr');

        inspeccionItem.innerHTML = `
            <td>${index + 1}</td>
            <td>${inspeccion.codigo}</td>
            <td>${inspeccion.fecha_inicio}</td>
            <td>${inspeccion.hora_inicio}</td>
            <td>${inspeccion.hora_fin}</td>
            <td>${inspeccion.observacion}</td>
            <td><button type="button" class="btn btn-danger" id="btn-eliminar-inspeccion-${index}"><i class='bx bx-trash-alt'></i></button></td>
        `;

        listaInspecciones.appendChild(inspeccionItem);

        // Agregar evento al botón de eliminar inspección
        const btnEliminarInspeccion = document.getElementById(`btn-eliminar-inspeccion-${index}`);
        btnEliminarInspeccion.addEventListener('click', (e) => {
            e.preventDefault();  // Evitar que se envíe el formulario
            eliminarInspeccion(index);
        });
    });
}

function eliminarInspeccion(index) {
    const listaInspecciones = document.getElementById('lista_inspecciones');
    listaInspecciones.deleteRow(index);
}

function obtenerHerramientas(cuadernoId) {
    fetch(`/protocolo/filtrar_herramientas`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: '' })
    })
        .then(response => response.json())
        .then(data => {
            if (data.herramientas) {
                mostrarHerramientas(data.herramientas);
            } else {
                console.error('Error al obtener herramientas:', data.error);
            }
        })
        .catch(error => {
            console.error('Error al obtener herramientas:', error);
        });
}

function mostrarHerramientas(herramientas) {
    const listaHerramientas = document.getElementById('lista_herramientas');
    listaHerramientas.innerHTML = '';

    herramientas.forEach((herramienta, index) => {
        const herramientaItem = document.createElement('tr');

        herramientaItem.innerHTML = `
            <td>${index + 1}</td>
            <td>${herramienta.nombre}</td>
            <td>${herramienta.funcionalidad}</td>
            <td><button type="button" class="btn btn-danger" id="btn-eliminar-herramienta-${index}"><i class='bx bx-trash-alt'></i></button></td>
        `;

        listaHerramientas.appendChild(herramientaItem);

        const btnEliminarHerramienta = document.getElementById(`btn-eliminar-herramienta-${index}`);
        btnEliminarHerramienta.addEventListener('click', (e) => {
            e.preventDefault();
            eliminarHerramienta(index);
        });
    });
}

function eliminarHerramienta(index) {
    const listaHerramientas = document.getElementById('lista_herramientas');
    listaHerramientas.deleteRow(index);
}


function obtenerVuelos(cuadernoId, inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();

    fetch(`/protocolo/filtrar_planes_vuelo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: filter })
    })
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById(listaId);
            lista.innerHTML = '';
            if (data.planes_vuelo.length > 0) {
                data.planes_vuelo.forEach(vuelo => {
                    const div = document.createElement("div");
                    div.classList.add("list-group-item");
                    div.textContent = `${vuelo.nombre} - ${vuelo.fecha}`;
                    div.onclick = () => seleccionarVuelo(vuelo);
                    lista.appendChild(div);
                });
                lista.style.display = "block"; // Mostrar el div de resultados
            } else {
                lista.style.display = "none"; // Ocultar el div de resultados
            }
        })
        .catch(error => {
            console.error('Error al obtener vuelos:', error);
        });
}

function seleccionarVuelo(vuelo) {
    const listaVuelos = document.getElementById('lista_vuelos');
    const filas = listaVuelos.getElementsByTagName('tr');

    // Verificar si el vuelo ya está en la lista
    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas[1].innerText === vuelo.nombre) {
            alert("El vuelo ya está en la lista.");
            return;
        }
    }

    const vueloItem = document.createElement('tr');
    const index = filas.length;

    vueloItem.innerHTML = `
        <td>${index + 1}</td>
        <td>${vuelo.nombre}</td>
        <td>${vuelo.fecha}</td>
        <td>${vuelo.duracion}</td>
        <td>${periodicidades[vuelo.periocidad]}</td>
        <td><button type="button" class="btn btn-danger" onclick="eliminarVuelo(this, '${vuelo.document_id}')"><i class='bx bx-trash-alt'></i></button></td>
    `;

    listaVuelos.appendChild(vueloItem);

    // Ocultar el vuelo de la lista de resultados
    const resultados = document.getElementById('resultados_vuelos');
    const vueloDiv = [...resultados.children].find(item => item.textContent.includes(vuelo.nombre));
    if (vueloDiv) {
        vueloDiv.style.display = "none";
    }

    // Limpiar el campo de búsqueda y los resultados
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div

}

function eliminarVuelo(button, document_id) {
    const fila = button.closest('tr');
    const listaVuelos = document.getElementById('lista_vuelos');
    listaVuelos.removeChild(fila);

    // Reindexar las filas
    const filas = listaVuelos.getElementsByTagName('tr');
    for (let i = 0; i < filas.length; i++) {
        filas[i].getElementsByTagName('td')[0].innerText = i + 1;
    }

    // Habilitar de nuevo el vuelo en la lista de resultados
    const resultados = document.getElementById('resultados_vuelos');
    const vuelo = [...resultados.children].find(item => item.textContent.includes(document_id));
    if (vuelo) {
        vuelo.style.display = "block";
    }
}

function obtenerDetectores(cuadernoId, inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();

    fetch(`/protocolo/filtrar_detectores`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: filter })
    })
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById(listaId);
            lista.innerHTML = '';
            if (data.detectores.length > 0) {
                data.detectores.forEach(detector => {
                    const div = document.createElement("div");
                    div.classList.add("list-group-item");
                    div.textContent = `${detector.nombre} - ${detector.fecha}`;
                    div.onclick = () => seleccionarDetector(detector);
                    lista.appendChild(div);
                });
                lista.style.display = "block"; // Mostrar el div de resultados
            } else {
                lista.style.display = "none"; // Ocultar el div de resultados
            }
        })
        .catch(error => {
            console.error('Error al obtener detectores:', error);
        });
}

function seleccionarDetector(detector) {
    const listaDetectores = document.getElementById('lista_detectores');
    const filas = listaDetectores.getElementsByTagName('tr');

    // Verificar si el detector ya está en la lista
    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas[1].innerText === detector.nombre) {
            alert("El detector ya está en la lista.");
            return;
        }
    }

    const detectorItem = document.createElement('tr');
    const index = filas.length;

    detectorItem.innerHTML = `
        <td>${index + 1}</td>
        <td>${detector.nombre}</td>
        <td>${detector.fecha}</td>
        <td>${detector.duracion}</td>
        <td>${periodicidades[detector.periocidad]}</td>
        <td><button type="button" class="btn btn-danger" onclick="eliminarDetector(this, '${detector.document_id}')"><i class='bx bx-trash-alt'></i></button></td>
    `;

    listaDetectores.appendChild(detectorItem);

    // Ocultar el detector de la lista de resultados
    const resultados = document.getElementById('resultados_detectores');
    const detectorDiv = [...resultados.children].find(item => item.textContent.includes(detector.nombre));
    if (detectorDiv) {
        detectorDiv.style.display = "none";
    }

    // Limpiar el campo de búsqueda y los resultados
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
}

function eliminarDetector(button, document_id) {
    const fila = button.closest('tr');
    const listaDetectores = document.getElementById('lista_detectores');
    listaDetectores.removeChild(fila);

    // Reindexar las filas
    const filas = listaDetectores.getElementsByTagName('tr');
    for (let i = 0; i < filas.length; i++) {
        filas[i].getElementsByTagName('td')[0].innerText = i + 1;
    }

    // Habilitar de nuevo el detector en la lista de resultados
    const resultados = document.getElementById('resultados_detectores');
    const detector = [...resultados.children].find(item => item.textContent.includes(document_id));
    if (detector) {
        detector.style.display = "block";
    }
}

function obtenerInspecciones(cuadernoId, inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();

    fetch(`/protocolo/filtrar_inspecciones_campo`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: filter })
    })
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById(listaId);
            lista.innerHTML = '';
            if (data.inspecciones_campo.length > 0) {
                data.inspecciones_campo.forEach(inspeccion => {
                    const div = document.createElement("div");
                    div.classList.add("list-group-item");
                    div.textContent = `${inspeccion.nombre} - ${inspeccion.fecha}`;
                    div.onclick = () => seleccionarInspeccion(inspeccion);
                    lista.appendChild(div);
                });
                lista.style.display = "block"; // Mostrar el div de resultados
            } else {
                lista.style.display = "none"; // Ocultar el div de resultados
            }
        })
        .catch(error => {
            console.error('Error al obtener inspecciones:', error);
        });
}

function seleccionarInspeccion(inspeccion) {
    const listaInspecciones = document.getElementById('lista_inspecciones');
    const filas = listaInspecciones.getElementsByTagName('tr');

    // Verificar si la inspección ya está en la lista
    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas[1].innerText === inspeccion.nombre) {
            alert("La inspección ya está en la lista.");
            return;
        }
    }

    const inspeccionItem = document.createElement('tr');
    const index = filas.length;

    inspeccionItem.innerHTML = `
        <td>${index + 1}</td>
        <td>${inspeccion.nombre}</td>
        <td>${inspeccion.fecha}</td>
        <td><button type="button" class="btn btn-danger" onclick="eliminarInspeccion(this, '${inspeccion.document_id}')"><i class='bx bx-trash-alt'></i></button></td>
    `;

    listaInspecciones.appendChild(inspeccionItem);

    // Ocultar la inspección de la lista de resultados
    const resultados = document.getElementById('resultados_inspecciones');
    const inspeccionDiv = [...resultados.children].find(item => item.textContent.includes(inspeccion.nombre));
    if (inspeccionDiv) {
        inspeccionDiv.style.display = "none";
    }

    // Limpiar el campo de búsqueda y los resultados
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
}

function eliminarInspeccion(button, document_id) {
    const fila = button.closest('tr');
    const listaInspecciones = document.getElementById('lista_inspecciones');
    listaInspecciones.removeChild(fila);

    // Reindexar las filas
    const filas = listaInspecciones.getElementsByTagName('tr');
    for (let i = 0; i < filas.length; i++) {
        filas[i].getElementsByTagName('td')[0].innerText = i + 1;
    }

    // Habilitar de nuevo la inspección en la lista de resultados
    const resultados = document.getElementById('resultados_inspecciones');
    const inspeccion = [...resultados.children].find(item => item.textContent.includes(document_id));
    if (inspeccion) {
        inspeccion.style.display = "block";
    }
}


function obtenerHerramientas(cuadernoId, inputId, listaId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toLowerCase();

    fetch(`/protocolo/filtrar_herramientas`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content') // Incluyendo el token CSRF en la cabecera
        },
        body: JSON.stringify({ cuaderno_id: cuadernoId, query: filter })
    })
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById(listaId);
            lista.innerHTML = '';
            if (data.herramientas.length > 0) {
                data.herramientas.forEach(herramienta => {
                    const div = document.createElement("div");
                    div.classList.add("list-group-item");
                    div.textContent = `${herramienta.nombre} - ${herramienta.funcionalidad}`;
                    div.onclick = () => seleccionarHerramienta(herramienta);
                    lista.appendChild(div);
                });
                lista.style.display = "block"; // Mostrar el div de resultados
            } else {
                lista.style.display = "none"; // Ocultar el div de resultados
            }
        })
        .catch(error => {
            console.error('Error al obtener herramientas:', error);
        });
}

function seleccionarHerramienta(herramienta) {
    const listaHerramientas = document.getElementById('lista_herramientas');
    const filas = listaHerramientas.getElementsByTagName('tr');

    // Verificar si la herramienta ya está en la lista
    for (let i = 0; i < filas.length; i++) {
        const celdas = filas[i].getElementsByTagName('td');
        if (celdas[1].innerText === herramienta.nombre) {
            alert("La herramienta ya está en la lista.");
            return;
        }
    }

    const herramientaItem = document.createElement('tr');
    const index = filas.length;

    herramientaItem.innerHTML = `
        <td>${index + 1}</td>
        <td>${herramienta.nombre}</td>
        <td>${herramienta.funcionalidad}</td>
        <td><button type="button" class="btn btn-danger" onclick="eliminarHerramienta(this, '${herramienta.document_id}')"><i class='bx bx-trash-alt'></i></button></td>
    `;

    listaHerramientas.appendChild(herramientaItem);

    // Ocultar la herramienta de la lista de resultados
    const resultados = document.getElementById('resultados_herramientas');
    const herramientaDiv = [...resultados.children].find(item => item.textContent.includes(herramienta.nombre));
    if (herramientaDiv) {
        herramientaDiv.style.display = "none";
    }

    // Limpiar el campo de búsqueda y los resultados
    resultados.innerHTML = "";
    resultados.style.display = "none";  // Ocultar el div
}

function eliminarHerramienta(button, document_id) {
    const fila = button.closest('tr');
    const listaHerramientas = document.getElementById('lista_herramientas');
    listaHerramientas.removeChild(fila);

    // Reindexar las filas
    const filas = listaHerramientas.getElementsByTagName('tr');
    for (let i = 0; i < filas.length; i++) {
        filas[i].getElementsByTagName('td')[0].innerText = i + 1;
    }

    // Habilitar de nuevo la herramienta en la lista de resultados
    const resultados = document.getElementById('resultados_herramientas');
    const herramienta = [...resultados.children].find(item => item.textContent.includes(document_id));
    if (herramienta) {
        herramienta.style.display = "block";
    }
}
