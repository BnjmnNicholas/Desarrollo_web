// recuperamos la tabla del DOM
let tabla = document.getElementById("tabla-artesanos");

// recuperamos los registros de la tabla
let registros = tabla.getElementsByTagName("tr");

// recorremos los registros
for (let i = 0; i < registros.length; i++) {
    // a cada registro le asignamos el enlace href = 'informacion-artesano.html'
    registros[i].addEventListener("click", () => {
        window.location.href = "informacion-artesano.html";
    });
    }


