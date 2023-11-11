let tabla = document.getElementById("tabla-artesanos");
let registros = tabla.getElementsByTagName("tr");

for (let i = 0; i < registros.length; i++) {
    let artesanoId = registros[i].getAttribute("data-id");

    console.log(artesanoId);
    registros[i].addEventListener("click", () => {
        window.location.href = "/detalle_artesano/" + artesanoId;
    });
}
