from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
import json
from validations import validador_nombre, validador_mail, validador_celular, validador_region, validador_comuna, validador_artesanias, validador_imagen
import re


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')




# ------------------------------------------------------------------------------------------
@app.route('/agregar_artesano', methods=['GET', 'POST'])
def agregar_artesano():
    
    error = None
    messages = []
    
    
    # recogemos los tipos de artesanias, regiones y comunas de la bbdd,
    # para mostrarlos en el formulario
    # artesanias = db.get_artesanias()
    artesanias = db.get_artesanias()     
    # creamos una lista con las artesanias
    lista_artesanias = []
    # recorremos las artesanias y las agregamos a la lista
    for artesania in artesanias:
        lista_artesanias.append(artesania[1])
        
    # dicc para regiones y comunas
    # regiones
    regiones = db.get_regiones()
    comunas = db.get_comunas()

    # Crear un diccionario para almacenar las regiones y sus comunas
    regiones_y_comunas = {}
    
    # Llenar el diccionario con las regiones y sus comunas correspondientes
    for region_id, region_nombre in regiones:
        # Filtrar las comunas que pertenecen a la región actual
        comunas_region = [comuna_nombre for comuna_id, comuna_nombre, comuna_region_id in comunas if comuna_region_id == region_id]
        regiones_y_comunas[region_nombre] = comunas_region

    # Convierte los datos a una cadena JSON
    regiones_y_comunas_json = json.dumps(regiones_y_comunas)
    
    
    if request.method == "GET":
        # Resto del código GET
        return render_template('agregar_artesano sinJs.html',
                               artesanias=lista_artesanias,
                               regiones_y_comunas=regiones_y_comunas,
                               regiones_y_comunas_json=regiones_y_comunas_json,
                               messages=messages)

    if request.method == "POST":
        nombre = request.form['nombre']
        mail = request.form['email']
        celular = request.form['celular']
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        artesania_1 = request.form.get('artesania_1')
        artesania_2 = request.form.get('artesania_2')
        artesania_3 = request.form.get('artesania_3')
        com_artesania_1 = request.form['comentario_artesania_1']
        com_artesania_2 = request.form['comentario_artesania_2']
        com_artesania_3 = request.form['comentario_artesania_3']

        errors = {
            "nombre": 'Por favor, ingrese un nombre válido',
            "email": 'Por favor, ingrese un correo electrónico válido',
            "celular": 'Por favor, ingrese un número de celular válido',
            "region": 'Por favor, seleccione una región',
            "comuna": 'Por favor, seleccione una comuna',
            "artesanias": 'Por favor, seleccione al menos una artesanía',
            "imagen": 'Por favor, ingrese una imagen válida'
        }

        if not validador_nombre(nombre):
            messages.append(errors["nombre"])
        if not validador_mail(mail):
            messages.append(errors["email"])
        if not validador_celular(celular):
            messages.append(errors["celular"])
        if not validador_region(region):
            messages.append(errors["region"])
        if not validador_comuna(comuna):
            messages.append(errors["comuna"])
        if not validador_artesanias(artesania_1, artesania_2, artesania_3):
            messages.append(errors["artesanias"])

        if len(messages) == 0:
            flash('El artesano ha sido registrado correctamente', 'success')
            
            # agregamos el registro a la base de datos
            # obtenemos el id de la comuna
            comuna_id = db.get_comuna_id(comuna)
            
            # obtenemos el id de las artesanias
            artesania_1_id = db.get_id_artesania(artesania_1)
            artesania_2_id = db.get_id_artesania(artesania_2)
            artesania_3_id = db.get_id_artesania(artesania_3)
            
            
            # obtenemos el ultimo id de la tabla artesano y sumamos 1
            last_id = db.get_last_id_artesanos() 
            id = last_id[0] + 1
            
            # creamos un diccionario json que almacena com_arrtesanias
            com_artesanias = {}
            com_artesanias[artesania_1] = com_artesania_1
            com_artesanias[artesania_2] = com_artesania_2
            com_artesanias[artesania_3] = com_artesania_3
            
            # pasamos el diccionario a string para poder almacenarlo en la bbdd
            com_artesanias_json = json.dumps(com_artesanias)
            
            
            # insertamos el artesano en la base bbdd artesanos
            db.insert_artesano(id = id, nombre = nombre, email = mail,
                               descripcion_artesania= com_artesanias_json,
                               celular = celular, comuna_id= comuna_id)
            
            # insertamos las artesanias en la bbdd artesano_tipo
            db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_1_id)
            db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_2_id)
            db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_3_id)
            
            
            # mandamos al usuario a la pagina de inicio
            return redirect(url_for('index'))
        
#        print(messages)
    
    # Resto del código...

        return render_template('agregar_artesano sinJs.html',
                            artesanias=lista_artesanias,
                            regiones_y_comunas=regiones_y_comunas,
                            regiones_y_comunas_json=regiones_y_comunas_json,
                            messages=messages)
    
# actualmente cuando se encuentran errores al enviar el formulario, se pierden los datos ingresados 
# en el formulario. Para solucionar esto se puede hacer de distintas formas (no lo hice por tiempo) 
# se puede usar Ajax, se puede enviar los inputs ingresados en el mismo render_template. 


# ------------------------------------------------------------------------------------------
    
@app.route('/listado_artesanos', methods=['GET'])
def listado_artesanos():
    # obtenemos los artesanos de la bbdd
    listado_artesanos = db.get_artesanos()
    
    print(listado_artesanos)
    
    # almacenamos todos los registros en una lista
    lista_artesanos = []
    for artesano in listado_artesanos:
        # a partir del id de la comuna obtenemos el nombre de la comuna
        comuna = db.get_comuna_nombre(artesano[2])
        
        # remplazamos el id de la comuna por su nombre
        artesano = list(artesano)
        artesano[2] = comuna[0]
        artesano = tuple(artesano)
        
        # agregamos el artesano a la lista
        lista_artesanos.append(artesano)
    
    print(lista_artesanos)
    
    return render_template('listado_artesanos.html', artesanos=lista_artesanos)

if __name__ == '__main__':
    app.run(debug=True)
