// obtenemos los elementos del DOM
let deportes_select_1 = document.getElementById("deporte_1");
let deportes_select_2 = document.getElementById("deporte_2");
let deportes_select_3 = document.getElementById("deporte_3");


// agregamos los deportes desde el archivo deportes.js 
for (let i = 1; i <= Object.keys(deportes_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = deportes_lista[i];
    deportes_select_1.appendChild(option);
}

// agregamos los mismos deportes a los select 2 y 3
for (let i = 1; i <= Object.keys(deportes_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = deportes_lista[i];
    deportes_select_2.appendChild(option);
}

for (let i = 1; i <= Object.keys(deportes_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = deportes_lista[i];
    deportes_select_3.appendChild(option);
}