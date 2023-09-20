// obtenemos los elementos del DOM
let artesania_select_1 = document.getElementById("artesania_1");
let artesania_select_2 = document.getElementById("artesania_2");
let artesania_select_3 = document.getElementById("artesania_3");


// agregamos las artesanias
for (let i = 1; i <= Object.keys(artesanias_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = artesanias_lista[i];
    artesania_select_1.appendChild(option);
}

// agregamos los mismos deportes a los select 2 y 3
for (let i = 1; i <= Object.keys(artesanias_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = artesanias_lista[i];
    artesania_select_2.appendChild(option);
}

for (let i = 1; i <= Object.keys(artesanias_lista).length; i++) {
    let option = document.createElement("option");
    option.value = i;
    option.text = artesanias_lista[i];
    artesania_select_3.appendChild(option);
}