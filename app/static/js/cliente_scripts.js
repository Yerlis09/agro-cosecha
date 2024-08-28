document.addEventListener("DOMContentLoaded", () => {
    const modalCliente = document.getElementById("modalCliente"),
        myModalRegistrar = document.getElementById("myModalRegistrar"),
        btn_cancelar = document.getElementById("btn-cancelar"),
        btn_update_cancelar = document.querySelectorAll(".btn_update_cancelar"),
        departamentoSelectRegister = document.getElementById('registro_departamento'),
        municipioSelectRegister = document.getElementById('registro_municipio'),
        deleteButtons = document.querySelectorAll('.delete-btn'),
        btn_guardar = document.getElementById('btn-guardar'),
        modalOkBtn = document.getElementById('modal-ok-btn'),
        clienteFormRegister = document.getElementById('cliente-form-register'),
        successModalRegister = document.getElementById('successModalRegister'),
        is_edit = document.getElementById('es_editar');
    let validarIsEdit = false;
    if (is_edit != null) {
        validarIsEdit = is_edit.value === "True";
    }


    // Obtener el token CSRF del meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    if (!validarIsEdit) {
        if (deleteButtons) {
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
    }

    if (btn_guardar) {
        btn_guardar.addEventListener('click', function () {
            const successModal = new bootstrap.Modal(document.getElementById('successModal')),
                modalOkBtn = document.getElementById('modal-ok-btn');

            document.getElementById('cliente-form').submit();
            // Mostrar modal de éxito si success es verdadero
            // Leer el valor de success desde el input oculto
            const success = document.getElementById('success-indicator').value === 'True';
            if (success) {
                successModal.show();
            }

            // Manejar click en el botón OK del modal de éxito
            if (modalOkBtn) {
                modalOkBtn.addEventListener('click', function () {
                    location.reload();
                });
            }
        });
    }

    if (clienteFormRegister) {
        clienteFormRegister.addEventListener('submit', function (event) {
            event.preventDefault();

            const formData = new FormData(clienteFormRegister);

            fetch(clienteFormRegister.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrf_token]').value
                }
            }).then(response => response.json())
                .then(data => {
                    if (data.success) {
                        myModalRegistrar.style.display = 'none';
                        successModalRegister.style.display = 'block';
                    } else {
                        // Manejo de errores
                        alert(`Error: ${data.error}`);
                        console.error('Error:', data.error);
                    }
                }).catch(error => {
                    alert(`Error: ${error.message}`);
                    console.error('Error:', error);
                });

            modalOkBtn.addEventListener('click', function () {
                successModalRegister.style.display = 'none';
                window.location.href = "/cliente/mostrar_registros_clientes"; // Redirige a la vista de clientes
                limpiarFormulario(clienteFormRegister);
            }, { once: true });
        });
    }

    function limpiarFormulario(form) {
        form.reset();
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.selectedIndex = 0;
        });
    }

    // Mostrar modal de registrar cliente
    function cargarMunicipios(departamento, selectElement, clienteMunicipio) {
        fetch("/cliente/fetch_municipios", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken  // Incluyendo el token CSRF en la cabecera
            },
            body: JSON.stringify({ departamento: departamento })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                selectElement.innerHTML = '';
                data.municipios.forEach(municipio => {
                    const option = document.createElement('option');
                    option.value = municipio.value;
                    option.textContent = municipio.label;
                    selectElement.appendChild(option);
                });

                if (clienteMunicipio) {
                    selectElement.value = clienteMunicipio;
                }
            })
            .catch(error => {
                console.error('Error al cargar municipios:', error);
            });
    }

    if (modalCliente) {
        modalCliente.addEventListener("click", e => {
            myModalRegistrar.style.display = "block";
            myModalRegistrar.classList.add("show");

            addDefaultOption(municipioSelectRegister);
            departamentoSelectRegister.addEventListener('change', () => {
                const departamentoSeleccionado = departamentoSelectRegister.value;
                municipioSelectRegister.disabled = !departamentoSeleccionado;
                if (departamentoSeleccionado) {
                    cargarMunicipios(departamentoSeleccionado, municipioSelectRegister);
                } else {
                    municipioSelectRegister.innerHTML = '<option value="">Seleccione</option>';
                }
            });
        });
    }


    // Manejar click en el botón cancelar del modal de registrar
    if (btn_cancelar) {
        btn_cancelar.addEventListener("click", e => {
            myModalRegistrar.style.display = "none";
            myModalRegistrar.classList.remove("show");
        });
    }

    // Manejar click en los botones cancelar de los modales de edición
    btn_update_cancelar.forEach(btn_update => {
        btn_update.addEventListener("click", e => {
            const myModalModificar = btn_update.closest('.modal');
            if (myModalModificar) {
                myModalModificar.style.display = "none";
                myModalModificar.classList.remove("show");
            }
        });
    });

    const addDefaultOption = (selectElement) => {
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = 'Seleccione';
        selectElement.appendChild(defaultOption);
    };

    document.querySelectorAll('select.departamento-select-update').forEach(selectElement => {
        const clienteId = selectElement.id.split('_').pop();
        const municipioSelectElement = document.getElementById(`municipio_${clienteId}`);
        const clienteMunicipio = municipioSelectElement.getAttribute('data-cliente-municipio');

        selectElement.addEventListener('change', () => {
            const departamentoSeleccionado = selectElement.value;
            municipioSelectElement.disabled = !departamentoSeleccionado;
            if (departamentoSeleccionado) {
                cargarMunicipios(departamentoSeleccionado, municipioSelectElement);
            } else {
                municipioSelectElement.innerHTML = '<option value="">Seleccione</option>';
            }
        });

        // Inicializar municipios para formularios de actualización ya cargados
        if (selectElement.value) {
            cargarMunicipios(selectElement.value, municipioSelectElement, clienteMunicipio);
        }
    });



    // Cerrar modal cuando se hace click fuera del modal
    window.addEventListener("click", e => {
        if (e.target === myModalRegistrar) {
            myModalRegistrar.style.display = "none";
            myModalRegistrar.classList.remove("show");
        }
        document.querySelectorAll('.modal').forEach(modal => {
            if (e.target === modal) {
                modal.style.display = "none";
                modal.classList.remove("show");
            }
        });
    });
});
