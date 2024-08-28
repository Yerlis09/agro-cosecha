const modalHerramienta = document.getElementById("modalHerramienta"),
    myModalRegistrar = document.getElementById("myModalRegistrar"),
    btn_cancelar = document.getElementById("btn-cancelar"),
    btn_edits = document.querySelectorAll(".edit-btn"),
    btn_update_cancelar = document.querySelectorAll(".btn_update_cancelar");


// Mostrar modal de registrar cliente
if (modalHerramienta) {
    modalHerramienta.addEventListener("click", e => {
        myModalRegistrar.style.display = "block";
        myModalRegistrar.classList.add("show");
    });
}

// Manejar click en los botones de editar
btn_edits.forEach(btn_edit => {
    btn_edit.addEventListener("click", e => {
        const targetModalId = btn_edit.getAttribute('data-target');
        const myModalModificar = document.querySelector(targetModalId);
        if (myModalModificar) {
            myModalModificar.style.display = "block";
            myModalModificar.classList.add("show");

        } else {
            console.error(`Modal with ID ${targetModalId} not found`);
        }
    });
});

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