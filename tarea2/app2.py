from flask import Flask, render_template, request, redirect, url_for, flash
from database import db
import json
from validations import validador_nombre, validador_mail,validador_celular, validador_region, validador_comuna, validador_artesanias, validador_imagen, new_name
import re


UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.secret_key = "s3cr3t_k3y"   #no hacer nuca esto, es solo para el ejemplo
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
        img_artesania_1 = request.files.get('artesania_1_img')
        img_artesania_2 = request.files.get('artesania_2_img')
        img_artesania_3 = request.files.get('artesania_3_img')
        
        print(img_artesania_1)
        print(img_artesania_2)
        print(img_artesania_3)

        errors = {
            "nombre": 'Por favor, ingrese un nombre válido',
            "email": 'Por favor, ingrese un correo electrónico válido',
            "celular": 'Por favor, ingrese un número de celular válido',
            "region": 'Por favor, seleccione una región',
            "comuna": 'Por favor, seleccione una comuna',
            "artesanias": 'Por favor, seleccione al menos una artesanía',
            "imagen_1": 'Por favor, ingrese una imagen 1 válida',
            "imagen_2": 'Por favor, ingrese una imagen 2 válida',
            "imagen_3": 'Por favor, ingrese una imagen 3 válida'
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
        # si no se selecciona una artesania, no se debe validar la imagen
        if not validador_imagen(img_artesania_1) and artesania_1 != None:   
            messages.append(errors["imagen_1"])
        if not validador_imagen(img_artesania_2) and artesania_2 != None:
            messages.append(errors["imagen_2"])
        if not validador_imagen(img_artesania_3) and artesania_3 != None:
            messages.append(errors["imagen_3"])

            
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
            if last_id == None:
                last_id = 0
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
            if artesania_1 != None:
                db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_1_id)
            if artesania_2 != None:
                db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_2_id)
            if artesania_3 != None:
                db.insert_artesano_tipo(artesano_id = id, tipo_artesania_id = artesania_3_id)
            
            #guardamos las imagenes en la carpeta uploads
            
            if img_artesania_1 != None:
                # imagen 1, generamos un nuevo nombre para la imagen
                filename = new_name(img=img_artesania_1, filename= img_artesania_1.filename, id=id)
                img_artesania_1.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
                
                # guardamos el nombre de la imagen en la bbdd
                last_id_foto = db.get_id_foto()
                if last_id_foto == None:
                    last_id_foto = 0
                id_foto = last_id_foto[0] + 1
                db.insert_foto(id = id_foto,
                               ruta_archivo = app.config['UPLOAD_FOLDER'] + '/' + filename,
                               nombre_archivo= filename,
                               artesano_id = id)
            
            if img_artesania_2 != None:
                # imagen 2, generamos un nuevo nombre para la imagen
                filename = new_name(img=img_artesania_2, filename= img_artesania_2.filename, id=id)
                img_artesania_2.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
                
                # guardamos el nombre de la imagen en la bbdd
                last_id_foto = db.get_id_foto()
                if last_id_foto == None:
                    last_id_foto = 0
                id_foto = last_id_foto[0] + 1
                db.insert_foto(id = id_foto,
                               ruta_archivo = app.config['UPLOAD_FOLDER'] + '/' + filename,
                               nombre_archivo= filename,
                               artesano_id = id)
            
            if img_artesania_3 != None:
                # imagen 3, generamos un nuevo nombre para la imagen
                filename = new_name(img=img_artesania_3, filename= img_artesania_3.filename, id=id)
                img_artesania_3.save(app.config['UPLOAD_FOLDER'] + '/' + filename)
                
                # guardamos el nombre de la imagen en la bbdd
                last_id_foto = db.get_id_foto()
                if last_id_foto == None:
                    last_id_foto = 0
                id_foto = last_id_foto[0] + 1
                db.insert_foto(id = id_foto,
                               ruta_archivo = app.config['UPLOAD_FOLDER'] + '/' + filename,
                               nombre_archivo= filename,
                               artesano_id = id)

            
            
            
            
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
    
    # almacenamos todos los registros en un diccionario
    diccionario_artesanos = {}
    
    for artesano in listado_artesanos:
        # a partir del id de la comuna obtenemos el nombre
        comuna = db.get_comuna_nombre(artesano[3])
        
        # a partir del id del artesano obtenemos sus tipos de artesanias
        artesanias_id = db.get_artesanias_artesano(artesano[0])
        
        # a partir de artesanias_id obtenemos los nombres de las artesanias
        artesanias = []
        for id in artesanias_id:
            artesania = db.get_artesania_nombre(id[0])
            artesanias.append(artesania[0])

        # a partir del id del artesano obtenemos las direcciones de las fotos
        rutas_fotos = db.get_fotos(artesano[0])
        
        # pasamos las direcciones a una lista
        rutas_fotos_list = []
        for ruta in rutas_fotos:
            rutas_fotos_list.append(ruta[0])
        
        # agregamos los datos al diccionario de artesanos {artesano_1_id : {nombre: nombre, celular: celular, comuna: comuna, lista_artesanias: artesanias, lista_rutas_fotos: fotos}}
        diccionario_artesanos[artesano[0]] = {'nombre': artesano[1], 'celular': artesano[2], 'comuna': comuna[0], 'lista_artesanias': artesanias, 'lista_rutas_fotos': rutas_fotos_list}
    print(diccionario_artesanos)
        
    return render_template('listado_artesanos.html', artesanos_data=diccionario_artesanos)
        
if __name__ == '__main__':
    app.run(debug=True)
