from flask import Flask, render_template, request,  flash
from database import db
from val import vh, va # validadores va:validador artesano vh: validador hincha
import json
import bleach

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
    
    #-----------------------------------------------------------------------------------------------
    #-----------------------------------Obtenemos los datos de la bbdd------------------------------
    
    
    messages = []  # este arreglo se usa para almacenar los mensajes de error o notificaciones
    
    
    # recogemos los tipos de artesanias, regiones y comunas de la bbdd,
    # para mostrarlos en el formulario
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
    
    #-----------------------------------------------------------------------------------------------
    #---------------------------------------Metodo GET----------------------------------------------

    if request.method == "GET":
        # Resto del código GET
        return render_template('agregar_artesano.html',
                               artesanias=lista_artesanias,
                               regiones_y_comunas=regiones_y_comunas,
                               regiones_y_comunas_json=regiones_y_comunas_json,
                               messages=messages)
        
        
    #-----------------------------------------------------------------------------------------------
    #---------------------------------------Metodo POST----------------------------------------------
    if request.method == "POST":
        
        # recogemos las variables del formulario
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
        

        errors = {
            "nombre": 'Por favor, ingrese un nombre válido',
            "email": 'Por favor, ingrese un correo electrónico válido',
            "celular": 'Por favor, ingrese un número de celular válido',
            "region": 'Por favor, seleccione una región',
            "comuna": 'Por favor, seleccione una comuna',
            "artesanias": 'Por favor, seleccione al menos una artesanía',
            "imagen_1": 'Por favor, ingrese una imagen 1 válida',
            "imagen_2": 'Por favor, ingrese una imagen 2 válida',
            "imagen_3": 'Por favor, ingrese una imagen 3 válida',
            "descripcion1": "Por favor, ingrese una descripción 1 válida",
            "descripcion2": "Por favor, ingrese una descripción 2 válida",
            "descripcion3": "Por favor, ingrese una descripción 3 válida",
            "registro": "El artesano ya se encuentra registrado en la base de datos",
        }


        # validamos los datos ingresados

        if not va.validador_nombre(nombre):
            messages.append(errors["nombre"])
            
        if not va.validador_mail(mail):
            messages.append(errors["email"])
            
        if not va.validador_celular(celular):
            messages.append(errors["celular"])
            
        if not va.validador_region(region):
            messages.append(errors["region"])
            
        if not va.validador_comuna(comuna):
            messages.append(errors["comuna"])
            
        if not va.validador_artesanias(artesania_1, artesania_2, artesania_3):
            messages.append(errors["artesanias"])
            

        if not va.validador_imagen(img_artesania_1) and artesania_1 != None:    
            # si no se selecciona una artesania, no se debe validar la imagen
            messages.append(errors["imagen_1"])
        if not va.validador_imagen(img_artesania_2) and artesania_2 != None:
            messages.append(errors["imagen_2"])
        if not va.validador_imagen(img_artesania_3) and artesania_3 != None:
            messages.append(errors["imagen_3"])

        if not va.validador_descripcion(com_artesania_1) and artesania_1 != None:
            messages.append(errors["descripcion1"])
        if not va.validador_descripcion(com_artesania_2) and artesania_2 != None:
            messages.append(errors["descripcion2"])
        if not va.validador_descripcion(com_artesania_3) and artesania_3 != None:
            messages.append(errors["descripcion3"])
            
        
        # validamos si el artesano ya se encuentra en la bbdd
        if db.validador_bbdd_artesano(nombre= nombre, email= mail, celular= celular, comuna_id= comuna):
            messages.append(errors["registro"])
        
        
        # si no hay errores, se agrega el artesano a la bbdd
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
            if va.validador_imagen(img_artesania_1) and artesania_1 != None:
                # imagen 1, generamos un nuevo nombre para la imagen
                filename = va.new_name(img=img_artesania_1, filename= img_artesania_1.filename, id=id)
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
            
            if va.validador_imagen(img_artesania_2) and artesania_2 != None:
                # imagen 2, generamos un nuevo nombre para la imagen
                filename = va.new_name(img=img_artesania_2, filename= img_artesania_2.filename, id=id)
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
            
            if va.validador_imagen(img_artesania_3) and artesania_3 != None:
                # imagen 3, generamos un nuevo nombre para la imagen
                filename = va.new_name(img=img_artesania_3, filename= img_artesania_3.filename, id=id)
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

            
            
            # mandamos al usuario a la pagina de inicio y le alertamos que el artesano se ha registrado correctamente
            messages.append('El artesano ha sido registrado correctamente')
            print(messages)
            return render_template('index.html', messages=messages)
        

        # si hay errores, se muestran en el formulario
        return render_template('agregar_artesano.html',
                            artesanias=lista_artesanias,
                            regiones_y_comunas=regiones_y_comunas,
                            regiones_y_comunas_json=regiones_y_comunas_json,
                            messages=messages)
    
# actualmente cuando se encuentran errores al enviar el formulario, se pierden los datos ingresados 
# en el formulario. Para solucionar esto se puede hacer de distintas formas (no lo hice por tiempo) 
# se puede usar Ajax, se puede enviar los inputs ingresados en el mismo render_template. 


# ------------------------------------------------------------------------------------------
@app.route('/agregar_hincha', methods=['GET', 'POST'])
def agregar_hincha():

    #-----------------------------------------------------------------------------------------------
    #-----------------------------------Obtenemos los datos de la bbdd------------------------------
    
    
    messages = []  # este arreglo se usa para almacenar los mensajes de error o notificaciones
    
    
    # recogemos los deportes de la bbdd
    deportes = db.get_deportes()
    
    # lista con los deportes
    lista_deportes = []
    
    # recorremos los deportes y los agregamos a la lista
    for deporte in deportes:
        lista_deportes.append(deporte[1])
        
    
    
    # recogemos los tipos de artesanias, regiones y comunas de la bbdd,
    # para mostrarlos en el formulario
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
    
    #-----------------------------------------------------------------------------------------------
    #---------------------------------------Metodo GET----------------------------------------------

    if request.method == "GET":
        # Resto del código GET
        return render_template('agregar_hincha.html',
                               deportes = lista_deportes,
                               regiones_y_comunas=regiones_y_comunas,
                               regiones_y_comunas_json=regiones_y_comunas_json,
                               messages=messages)
        
        
    #-----------------------------------------------------------------------------------------------
    #---------------------------------------Metodo POST----------------------------------------------
    if request.method == "POST":
        
        # recogemos las variables del formulario
        nombre = request.form['nombre']
        mail = request.form['email']
        celular = request.form['celular']
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        transporte = request.form.get('transporte')
        deporte_1 = request.form.get('deporte_1')
        deporte_2 = request.form.get('deporte_2')
        deporte_3 = request.form.get('deporte_3')
        comentario = request.form['comentario']
        
        
        id_deporte_1 = db.get_id_deporte(deporte_1)
        print(id_deporte_1)
        
        
        errors = {
            "nombre": 'Por favor, ingrese un nombre válido',
            "email": 'Por favor, ingrese un correo electrónico válido',
            "celular": 'Por favor, ingrese un número de celular válido',
            "region": 'Por favor, seleccione una región',
            "comuna": 'Por favor, seleccione una comuna',
            "transporte": 'Por favor, seleccione un medio de transporte',
            "deporte": 'Por favor, seleccione al menos un deporte',
            "comentario": 'Por favor, ingrese un comentario válido',
            "registro": "El artesano ya se encuentra registrado en la base de datos",
        }


        # validamos los datos ingresados

        if not vh.validador_nombre(nombre):
            messages.append(errors["nombre"])
            
        if not vh.validador_mail(mail):
            messages.append(errors["email"])
            
        if not vh.validador_celular(celular):
            messages.append(errors["celular"])
            
        if not vh.validador_region(region):
            messages.append(errors["region"])
            
        if not vh.validador_comuna(comuna):
            messages.append(errors["comuna"])
            
        if not vh.validador_deportes(deporte_1, deporte_2, deporte_3):
            messages.append(errors["deporte"])
        
        if not vh.validador_comentario(comentario):
            messages.append(errors["comentario"])
        
        if not vh.validador_transporte(transporte):
            messages.append(errors["transporte"])
            
            
        
        # validamos si el artesano ya se encuentra en la bbdd
        if db.validador_bbdd_hincha(nombre= nombre, email= mail, celular= celular, comuna_id= comuna):
            messages.append(errors["registro"])
        
        
        # si no hay errores, se agrega el artesano a la bbdd
        if len(messages) == 0:
            flash('El artesano ha sido registrado correctamente', 'success')
            
            # agregamos el registro a la base de datos
            # obtenemos el id de la comuna
            comuna_id = db.get_comuna_id(comuna)
            
            
            
            # obtenemos el ultimo id de la tabla artesano y sumamos 1
            last_id = db.get_last_id_hinchas() 
            if last_id == None:
                last_id = 0
                id = last_id + 1
            else:
                id = last_id[0] + 1
            
            # obtenemos el id de los deportes
            deporte_1_id = db.get_id_deporte(deporte_1)
            deporte_2_id = db.get_id_deporte(deporte_2)
            deporte_3_id = db.get_id_deporte(deporte_3)
            
                
            # insertamos el hincha en la bbdd hincha
            db.insert_hincha(id = id,
                             comuna_id = comuna_id,
                             transporte = transporte,
                             nombre = nombre,
                             email = mail,
                             celular = celular,
                             comentario = comentario)
            
            if deporte_1_id != None:
                db.insert_hincha_deporte(hincha_id = id, deporte_id = deporte_1_id)
            if deporte_2_id != None:
                db.insert_hincha_deporte(hincha_id = id, deporte_id = deporte_2_id)
            if deporte_3_id != None:
                db.insert_hincha_deporte(hincha_id = id, deporte_id = deporte_3_id)
    
            # mandamos al usuario a la pagina de inicio y le alertamos que el artesano se ha registrado correctamente
            messages.append('El hincha ha sido registrado correctamente')
            print(messages)
            return render_template('index.html', messages=messages)
        

        # si hay errores, se muestran en el formulario
        return render_template('agregar_hincha.html',
                            artesanias=lista_artesanias,
                            regiones_y_comunas=regiones_y_comunas,
                            regiones_y_comunas_json=regiones_y_comunas_json,
                            messages=messages)
    
# actualmente cuando se encuentran errores al enviar el formulario, se pierden los datos ingresados 
# en el formulario. Para solucionar esto se puede hacer de distintas formas (no lo hice por tiempo) 
# se puede usar Ajax, se puede enviar los inputs ingresados en el mismo render_template. 


# ------------------------------------------------------------------------------------------   

@app.route('/listado_hinchas', methods=['GET', 'POST'])
def listado_hinchas():
    
    #-----------------------------------------------------------------------------------------------
    #-----------------------------------Obtenemos los datos de la bbdd------------------------------
    
    # obtenemos los artesanos de la bbdd
    listado_hinchas = db.get_hinchas()
    len_data = len(listado_hinchas)    
    
    #-----------------------------------------------------------------------------------------------
    #-------------------------------------------Paginación------------------------------------------
    # Obtiene el número de página de la consulta de la URL, por ejemplo: /listado_hinchas?page=1
    page = request.args.get('page', 1, type=int)
    
    # Realiza la paginación
    items_per_page = 5
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_data = listado_hinchas[start:end]
    listado_hinchas = paginated_data
    
    
    # comentario: hay un detalle de diseño que es que si el numero de artesanos es muy grande,
    # la paginacion se vera muy larga, se puede solucionar de distintas formas, por ejemplo
    # se puede agregar un buscador, o se puede agregar un filtro por regiones. Lo dejé así por tiempo.
    

    
    #-----------------------------------------------------------------------------------------------
    #----------------------------------------Procesamiento------------------------------------------
    # almacenamos todos los registros en un diccionario
    diccionario_hinchas = {}
    
    for hincha in listado_hinchas:
        # sql = "SELECT id, nombre, celular, comuna_id FROM hincha"
        
        # a partir del id de la comuna obtenemos el nombre
        comuna = db.get_comuna_nombre(hincha[3])
        
        # a partir del id del artesano obtenemos sus tipos de artesanias
        deportes_id = db.get_deportes_hincha(hincha[0])
        
        # a partir de artesanias_id obtenemos los nombres de las artesanias
        deportes = []
        for id in deportes_id:
            deporte = db.get_deporte_nombre(id[0])
            deportes.append(deporte[0])

        
        # agregamos los datos al diccionario de artesanos.
        diccionario_hinchas[hincha[0]] = {'id': hincha[0],
                                              'nombre': hincha[1],
                                              'celular': hincha[2],
                                              'comuna': comuna[0],
                                              'lista_deportes': deportes,
                                              'transporte': hincha[4],}
    
    #print(diccionario_artesanos)
    
    
    return render_template('listado_hinchas.html', hinchas_data=diccionario_hinchas,
                           len_data=len_data)
    

# ------------------------------------------------------------------------------------------    

@app.route('/listado_artesanos', methods=['GET'])
def listado_artesanos():
    
    #-----------------------------------------------------------------------------------------------
    #-----------------------------------Obtenemos los datos de la bbdd------------------------------
    
    # obtenemos los artesanos de la bbdd
    listado_artesanos = db.get_artesanos()
    len_data = len(listado_artesanos)    
    
    #-----------------------------------------------------------------------------------------------
    #-------------------------------------------Paginación------------------------------------------
    # Obtiene el número de página de la consulta de la URL, por ejemplo: /listado_artesanos?page=1
    page = request.args.get('page', 1, type=int)
    
    # Realiza la paginación
    items_per_page = 5
    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_data = listado_artesanos[start:end]
    listado_artesanos = paginated_data
    
    
    # comentario: hay un detalle de diseño que es que si el numero de artesanos es muy grande,
    # la paginacion se vera muy larga, se puede solucionar de distintas formas, por ejemplo
    # se puede agregar un buscador, o se puede agregar un filtro por regiones. Lo dejé así por tiempo.
    

    
    #-----------------------------------------------------------------------------------------------
    #----------------------------------------Procesamiento------------------------------------------
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
        
        # agregamos los datos al diccionario de artesanos.
        diccionario_artesanos[artesano[0]] = {'id': artesano[0],
                                              'nombre': artesano[1],
                                              'celular': artesano[2],
                                              'comuna': comuna[0],
                                              'lista_artesanias': artesanias,
                                              'lista_rutas_fotos': rutas_fotos_list}
    
    #print(diccionario_artesanos)
    
    
    return render_template('listado_artesanos.html', artesanos_data=diccionario_artesanos,
                           len_data=len_data)
    

# ------------------------------------------------------------------------------------------

@app.route('/detalle_artesano/<int:artesano_id>', methods=['GET'])
def detalle_artesano(artesano_id):
    #artesano = db.get_artesano_by_id(artesano_id)  # Asume que tienes una función para obtener un artesano por su ID
    #print(artesano_id)
    
    # escapamos el input
    artesano_id = bleach.clean(str(artesano_id))
    artesano_id = int(artesano_id)

    diccionario_artesano = {}
    
    data_artesano = db.get_artesano_by_id(artesano_id)
    # "SELECT id, nombre, celular, comuna_id FROM artesano
    
    # obtenemos los datos del artesano: Id, nombre, celular, comuna, tipos de artesanias y fotos.
    
    comuna = db.get_comuna_nombre(data_artesano[3])[0]
    
    region = db.get_region_nombre_by_comuna(data_artesano[3])[0]
    
    email = data_artesano[4]
    
    descripcion_artesanias = data_artesano[5]
    
    # a partir del id del artesano obtenemos sus tipos de artesanias
    artesanias_id = db.get_artesanias_artesano(artesano_id)
    
    # a partir de artesanias_id obtenemos los nombres de las artesanias
    artesanias = []
    for id in artesanias_id:
        artesania = db.get_artesania_nombre(id[0])
        artesanias.append(artesania[0])

    # a partir del id del artesano obtenemos las direcciones de las fotos
    rutas_fotos = db.get_fotos(artesano_id)
    
    # pasamos las direcciones a una lista
    rutas_fotos_list = []
    for ruta in rutas_fotos:
        rutas_fotos_list.append(ruta[0])
        
    region = db.get_region_nombre_by_comuna(data_artesano[3])[0]
#    print('region: ',region)
    
    # agregamos los datos al diccionario de artesanos.
    diccionario_artesano[artesano_id] = {   'id': artesano_id,
                                            'nombre': data_artesano[1],
                                            'celular': data_artesano[2],
                                            'email': email,
                                            'region':region,
                                            'comuna': comuna,
                                            'lista_artesanias': artesanias,
                                            'descripcion_artesanias': descripcion_artesanias,
                                            'lista_rutas_fotos': rutas_fotos_list}
    
    print(diccionario_artesano)
    
    return render_template('detalle_artesano.html', artesano=diccionario_artesano)

@app.route('/detalle_hincha/<int:hincha_id>', methods=['GET'])
def detalle_hincha(hincha_id):
    #artesano = db.get_artesano_by_id(artesano_id)  # Asume que tienes una función para obtener un artesano por su ID
    #print(artesano_id)
    
    # escapamos el input
    hincha_id = bleach.clean(str(hincha_id))
    hincha_id = int(hincha_id)
    
    print(hincha_id)
    
    diccionario_hincha = {}
    
    data_hincha = db.get_hincha_by_id(hincha_id)
    # SELECT SELECT id, nombre, email, celular, comuna_id, modo_transporte, comentarios
    
    # obtenemos los datos del hincha: id, nombre, celular, comuna_id, modo_transporte, comentarios
    
    email = data_hincha[2]
    
    comuna = db.get_comuna_nombre(data_hincha[4])[0]
    
    region = db.get_region_nombre_by_comuna(data_hincha[4])[0]
    
    # a partir del id del hincha obtenemos los id de los deportes
    deportes_id = db.get_deportes_hincha(hincha_id)
    
    # a partir de deportes_id obtenemos los nombres de los deportes
    deportes = []
    for id in deportes_id:
        deporte = db.get_deporte_nombre(id[0])
        deportes.append(deporte[0])


    
    # agregamos los datos al diccionario de artesanos.
    diccionario_hincha[hincha_id] = {   'id': hincha_id,
                                        'nombre': data_hincha[1],
                                        'celular': data_hincha[3],
                                        'email': email,
                                        'region': region,
                                        'comuna': comuna,
                                        'lista_deportes': deportes}
    
    print(diccionario_hincha)
    
    return render_template('detalle_hincha.html', hincha=diccionario_hincha)


@app.route('/graficos', methods=['GET'])
def graficos():
    return render_template('graficos.html')

        
if __name__ == '__main__':
    app.run(debug=True)
