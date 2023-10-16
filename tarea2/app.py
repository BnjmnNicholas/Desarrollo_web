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
    
    if request.method == "GET":    
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

        print(regiones_y_comunas)
        # Convierte los datos a una cadena JSON
        regiones_y_comunas_json = json.dumps(regiones_y_comunas)

        
        return render_template('agregar_artesano sinJs.html',
                               artesanias=lista_artesanias,
                               regiones_y_comunas=regiones_y_comunas,
                               regiones_y_comunas_json=regiones_y_comunas_json)
        
    elif request.method == "POST":
        # realizamos la validación por parte del servidor

        # obtenemos los inputs del formulario
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
            flash(errors["nombre"], 'error')
        elif not validador_mail(mail):
            flash(errors["email"], 'error')
        elif not validador_celular(celular):
            flash(errors["celular"], 'error')
        elif not validador_region(region):
            flash(errors["region"], 'error')
        elif not validador_comuna(comuna):
            flash(errors["comuna"], 'error')
        elif not validador_artesanias(artesania_1, artesania_2, artesania_3):
            flash(errors["artesanias"], 'error')
        elif not validador_imagen(request.form['imagen']):
            flash(errors["imagen"], 'error')
        else:
            flash('El artesano ha sido registrado correctamente', 'success')
            return redirect(url_for('index'))
        
        return redirect(url_for('agregar_artesano'))
        
    

    
@app.route('/listado_artesanos')
def listado_artesanos():
    return render_template('listado_artesanos.html')

if __name__ == '__main__':
    app.run(debug=True)
