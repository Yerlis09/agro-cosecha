const body = document.querySelector("body"),
    sidebar = document.querySelector(".sidebar"),
    toggle = document.querySelector(".toggle"),
    salirButton = document.querySelector(".salir-button");

toggle.addEventListener("click", () => {
    sidebar.classList.toggle("close");
});

