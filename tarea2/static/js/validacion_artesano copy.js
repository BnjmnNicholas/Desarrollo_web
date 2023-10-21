// validacion formulario
const validarForm = () => {

    // funciones auxiliares para validar
    const validadorMail = (mail) => {
        const regex = /^\S+@\S+\.\S+$/;
        // esta regex valida que el correo sea con el formato "string+@+string.string" es bastante sencilla
        // no quise agregar una más compleja porque creo que no es el foco.
        return regex.test(mail);
      };

    // funcion que valida el nombre, debe haber nombre, largo minimo 3 y maximo 80.
    const validadorNombre = (nombre) => nombre && nombre.length > 3 && nombre.length < 80;

    // funcion que valida que se seleccione almenos algun deporte y máximo 3 por la estructura
    const validadorArtesanias = (artesania_1, artesania_2, artesania_3) => artesania_1 || artesania_2 || artesania_3;

    // funcion que valida si hay una imagen, valida que sea tipo imagen
    const validadorImagen = (imagen) => imagen && imagen.includes(".jpg") || imagen.includes(".png") || imagen.includes(".jpeg");

    // funcion que valida que se haya seleccionado una region 
    const validadorRegion = (region) => region;

    // funcion que valida que se haya seleccionado una comuna
    const validadorComuna = (comuna) => comuna;

    // funcion que valida que se haya un transporte
    const validadorTransporte = (transporte) => transporte;

    // funcion que valida que se haya ingresado un telefono con formato correspondiente o que simplemente
    // no haya telefono
    const validadorCelular = (celular) => celular.length === 0 || /^(\+)?(\d{9,11})$/.test(celular);
      // la Regex indica que puede  iniciar con '+' y debe tener entre 9  y 11 numeros


  
    // obtener inputs del DOM por el ID
    let emailInput = document.getElementById("email");
    let nombreInput = document.getElementById("nombre");
    let artesania_1_Input = document.getElementById("artesania_1");
    let artesania_2_Input = document.getElementById("artesania_2");
    let artesania_3_Input = document.getElementById("artesania_3");
    let artesania_1_img = document.getElementById("artesania_1_img");
    let artesania_2_img = document.getElementById("artesania_2_img");
    let artesania_3_img = document.getElementById("artesania_3_img");
    let region_input = document.getElementById("region");
    let comuna_input = document.getElementById("comuna");
    let celular_input = document.getElementById("celular");


    let errorElement = document.getElementById("error");
    let errorList = document.getElementById("lista-errores");


    // creamos una lista para almacenar los errores
    let errores = [];


    // validamos input por input
    //------------------------------Validacion Nombre, Mail y Celular-----------------------------
    if (nombreInput.value.length === 0) {
        errores.push("Falta agregar un Nombre")
        nombreInput.style.borderColor = "red"; 
    }
    else {
        if (!validadorNombre(nombreInput.value)) {
            // agregamos el error a lista errores
            errores.push("Nombre no valido")
            nombreInput.style.borderColor = "red";
        }
        else {
            nombreInput.style.borderColor = "";
        }
    }

    if (emailInput.value.length === 0) {
        errores.push("Falta agregar Email")
        emailInput.style.borderColor = "red"; 
    }
    else {
        if (!validadorMail(emailInput.value)) {
            // agregamos el error a lista errores
            errores.push("Email no valido")
            emailInput.style.borderColor = "red";
        }
        else {
            emailInput.style.borderColor = "";
        }
    }

    if (celular_input.value.length === 0)  {
        errores.push("Falta agregar un Celular")
        nombreInput.style.borderColor = "red"; 
    }  
    else{
        if (!validadorCelular(celular_input.value)) {
            // agregamos el error a lista errores
            errores.push("Celular no valido")
            celular_input.style.borderColor = "red"; 
        } 
        else {
            celular_input.style.borderColor = "";
        };
    }
    //------------------------------Validacion Region y Comuna------------------------------------
    if (!validadorRegion(region_input.value)) {
        // agregamos el error a lista errores
        errores.push("Debes escoger una region")
        region_input.style.borderColor = "red"; 
        } else {
        region_input.style.borderColor = "";
        };


    if (!validadorComuna(comuna_input.value)) {
        // agregamos el error a lista errores
        errores.push("Debes escoger una comuna")
        comuna_input.style.borderColor = "red"; 
        } else {
        comuna_input.style.borderColor = "";
        };
    //------------------------------Validacion Artesanias------------------------------------------
    if (!validadorArtesanias(artesania_1_Input.value, artesania_2_Input.value, artesania_3_Input.value)) {
        // agregamos el error a lista errores
        errores.push("Debes agregar al menos una artesania")
        artesania_1_Input.style.borderColor = "red"; 
        artesania_2_Input.style.borderColor = "red";
        artesania_3_Input.style.borderColor = "red";
        } else {
            artesania_1_Input.style.borderColor = "";
            artesania_2_Input.style.borderColor = "";
            artesania_3_Input.style.borderColor = "";
        };


    // validador de imagen, si se agrega artesania 1 debe tener su imagen respectiva
    if (artesania_1_Input.value && !validadorImagen(artesania_1_img.value)) {
        // agregamos el error, debes agregar una imagen para la artesania 1!
        errores.push("Debes agregar una imagen para la artesania 1")
        // cambiamos el estilo de artesania_1_img
        artesania_1_img.style.borderColor = "red";
    } else {
        artesania_1_img.style.borderColor = "";
    };


    // validador de imagen, si se agrega artesania 2 debe tener su imagen respectiva
    if (artesania_2_Input.value && !validadorImagen(artesania_2_img.value)) {
        // agregamos el error, debes agregar una imagen para la artesania 2!
        errores.push("Debes agregar una imagen para la artesania 2")
        // cambiamos el estilo artesania_2_img
        artesania_2_img.style.borderColor = "red";
    } else {
        artesania_2_img.style.borderColor = "";
    };


    // validador de imagen, si se agrega artesania 3 debe tener su imagen respectiva
    if (artesania_3_Input.value && !validadorImagen(artesania_3_img.value)) {
        // agregamos el error, debes agregar una imagen para la artesania 3!
        errores.push("Debes agregar una imagen para la artesania 3")
        // cambiamos el estilo artesania_3_img
        artesania_3_img.style.borderColor = "red";
    } else {
        artesania_3_img.style.borderColor = "";
    };

    //--------------------------------Fin Validaciones ------------------------------------------


    if (errores.length === 0) {
        // borramos los errores anteriores
        errorList.innerHTML = ""
        //mostramos el div de confirmacion
        let confirmacion = document.getElementById("confirmacion");
        confirmacion.style.display = "block";

        // bajamos a la seccion de confirmacion
        window.location.href = "#confirmacion";
    }

    else {
        // si hay errores los mostramos
        // borramos los errores anteriores
        errorList.innerHTML = ""
        // creamos un elemento li por cada error
        errores.forEach(error => {
            let li = document.createElement("li")
            li.innerText = error
            errorList.appendChild(li)
        });
        // mostramos el error
        errorElement.style.display = "block";
        // errores en color rojo
        errorList.style.color = "red";
        // subimos la pagina a la seccion de error
        window.location.href = "#error";
    };
};


  
// recuperamos el boton que valida el formulario
let submitBtn = document.getElementById("envio");
submitBtn.addEventListener("click", validarForm);



// esta seccion se despliega cuando el formulario es valido
        
let confirmoBtn = document.getElementById("confirmar");
let noquieroBtn = document.getElementById("cancelar");

confirmoBtn.addEventListener("click", () => {
    window.location.href = "index.html";
    alert("Hemos recibido el registro del Artesano. Muchas gracias.")
}
);


noquieroBtn.addEventListener("click", () => {
    alert("No se ha registrado el Artesano, puedes modificar el formulario.")
    // ocultamos el div de confirmacion
    confirmacion.style.display = "none";
}
);