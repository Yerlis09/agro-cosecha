document.addEventListener("DOMContentLoaded", function () {
        containerFormLogin = document.getElementById("loginForm"),
        flashMessages = document.querySelector(".flash-messages");

    // Mostrar formulario de inicio de sesión si hay mensajes flash
    if (flashMessages && flashMessages.children.length > 0) {
        containerFormLogin.classList.remove("hide");
        containerFormRegister.classList.add("hide");
    }
});
