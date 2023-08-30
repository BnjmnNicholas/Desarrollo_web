//validar formulario hincha


// validaremos todas las entradas por separado y luego revisaremos todo en la función general val form.







function getRegion(region){

    let regionPlaceholder = document.querySelector("#region")
    let comunaPlaceholder = document.querySelector("#comuna")
    let comunasDropDown = document.querySelector("#comunas")

    regionPlaceholder.innerHTML = "";
    comunaPlaceholder.innerHTML = "";

    if(region.trim() === ""){
        comunasDropDown.disable = true;
        comunasDropDown.selectorIndex = 0;
        return false;
    }


    fetch("regiones-comunas.json")
    .then(function(response){
        return response.json();
    })
    .then(function(data){
        let comunas = data[region]
        let out = "";
        out += `<option value=""> Elegir comuna</option`;
        for(let comuna of comunas){
            out += `<option value="${comuna}">${comuna}</option>`;
        }
        comunasDropDown.innerHTML = out;
        comunasDropDown.disabled = false;
        regionPlaceholder.innerHTML = region;
    })
}

function getcomuna(comuna){
    return document.querySelector("#comuna").innerHTML = comuna 
} 