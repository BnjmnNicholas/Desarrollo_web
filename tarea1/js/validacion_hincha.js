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
    const validadorDeportes = (deporte_1, deporte_2, deporte_3) => deporte_1 || deporte_2 || deporte_3;

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
    let deporte_1_Input = document.getElementById("deporte_1");
    let deporte_2_Input = document.getElementById("deporte_2");
    let deporte_3_Input = document.getElementById("deporte_3");
    let region_input = document.getElementById("region");
    let comuna_input = document.getElementById("comuna");
    let transporte_input = document.getElementById("transporte");
    let celular_input = document.getElementById("celular");
    let comentario_input = document.getElementById("comentario");
    

    let errorElement = document.getElementById("error");
    let errorList = document.getElementById("lista-errores");
    
    
    // creamos una lista para almacenar los errores
    let errores = [];
    
    
    // validamos input por input

    //------------------------------Validacion Deportes------------------------------------------
    if (!validadorDeportes(deporte_1_Input.value, deporte_2_Input.value, deporte_3_Input.value)) {
        // agregamos el error a lista errores
        errores.push("Debes escoger al menos un deporte")
        deporte_1_Input.style.borderColor = "red"; 
        deporte_2_Input.style.borderColor = "red";
        deporte_3_Input.style.borderColor = "red";
        } 
    else {
            deporte_1_Input.style.borderColor = "";
            deporte_2_Input.style.borderColor = "";
            deporte_3_Input.style.borderColor = "";
    };
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

    //------------------------------Validacion Transporte------------------------------------------
    if (!validadorTransporte(transporte_input.value)) {
        // agregamos el error a lista errores
        errores.push("Debes seleccionar transporte")
        transporte_input.style.borderColor = "red"; 
        } else {
        transporte_input.style.borderColor = "";
        };
    //--------------------------------Fin Validaciones --------------------------------------------



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
    alert("Hemos recibido el registro de Hincha. Muchas gracias.")
}
);


noquieroBtn.addEventListener("click", () => {
    alert("No se ha registrado el Hincha, puedes modificar el formulario.")
    // ocultamos el div de confirmacion
    confirmacion.style.display = "none";
}
);