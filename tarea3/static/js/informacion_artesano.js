// recuperamos las imagenes de la tabla con alt="imagen1"
let imagenes = document.querySelectorAll("img[alt='foto']");



// recorremos las imagenes
for (let i = 0; i < imagenes.length; i++) {
    // a cada imagen le asignamos el evento click
    imagenes[i].addEventListener("click", () => {
        // se abre la imagen redimensionada
        window.open(imagenes[i].src, "imagen", "width=1280,height=1024");
    });
}