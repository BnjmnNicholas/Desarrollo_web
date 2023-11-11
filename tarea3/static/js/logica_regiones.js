// Agregamos un event listener al select de regiones
document.getElementById("region").addEventListener("change", function () {
    // Obtenemos el valor de la región seleccionada
    let region = this.value;
    // Obtén el select de comunas
    let comunas_select = document.getElementById("comuna");
    
    // Borramos las opciones anteriores
    comunas_select.innerHTML = "";
    
    // Verificamos si se ha seleccionado una región
    if (region !== "") {
        // Iteramos sobre las comunas de la región seleccionada
        let comunas = regiones_y_comunas[region];
        for (let i = 0; i < comunas.length; i++) {
            let option = document.createElement("option");
            option.value = comunas[i];
            option.text = comunas[i];
            comunas_select.appendChild(option);
        }
    } else {
        // Si no se ha seleccionado ninguna región, mostramos un mensaje predeterminado
        let defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Seleccionar comuna";
        comunas_select.appendChild(defaultOption);
    }
});



