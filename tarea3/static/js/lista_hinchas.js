let tabla = document.getElementById("tabla-hinchas");
let registros = tabla.getElementsByTagName("tr");

for (let i = 0; i < registros.length; i++) {
    let hinchaId = registros[i].getAttribute("data-id");

    console.log(hinchaId);
    registros[i].addEventListener("click", () => {
        window.location.href = "/detalle_artesano/" + hinchaId;
    });
}
