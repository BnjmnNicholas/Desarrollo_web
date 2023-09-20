// obtenemos los elementos del DOM
let region_select = document.getElementById("region");
let comunas_select = document.getElementById("comuna");

// agregamos las regiones desde el archivo regiones_comunas.js 
// iteramos sobre Object.keys(regiones_comunas) agregando las llaves como opciones
for (let i = 0; i < Object.keys(regionesComunas).length; i++) {
    let option = document.createElement("option");
    option.value = Object.keys(regionesComunas)[i];
    option.text = Object.keys(regionesComunas)[i];
    region_select.appendChild(option);
}


// agregamos las comunas en funcion de la region seleccionada
// agregamos un event listener al select de regiones
region_select.addEventListener("change", function () {
    // obtenemos el valor de la region seleccionada
    let region = region_select.value;
    // borramos las opciones anteriores
    comunas_select.innerHTML = "";
    // iteramos sobre las comunas de la region seleccionada
    for (let i = 0; i < regionesComunas[region].length; i++) {
        let option = document.createElement("option");
        option.value = regionesComunas[region][i];
        option.text = regionesComunas[region][i];
        comunas_select.appendChild(option);
    }
}
);
