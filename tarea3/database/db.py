import pymysql


def getConnection():
  conn = pymysql.connect(
    db='tarea2',
    user='cc5002',
    passwd='programacionweb',
    host='localhost',
    charset='utf8'
  )
  return conn


def get_usuario(conn, username):
  sql = "SELECT id, username, password, email FROM usuarios WHERE username=%s"
  cursor = conn.cursor()
  cursor.execute(sql, (username,))
  conn.commit()
  usuario = cursor.fetchone()
  return usuario

def get_deportes():
    conn = getConnection()
    sql = "SELECT id, nombre FROM deporte"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    deportes = cursor.fetchall()
    return deportes



def get_artesanias():
    conn = getConnection()    
    sql = "SELECT id, nombre FROM tipo_artesania"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    artesanias = cursor.fetchall()
    return artesanias

def get_regiones():
    conn = getConnection()    
    sql = "SELECT id, nombre FROM region"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    regiones = cursor.fetchall()
    return regiones

def get_comunas():
    conn = getConnection()    
    sql = "SELECT id, nombre, region_id FROM comuna"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    comunas = cursor.fetchall()
    return comunas
  

  
  
def get_artesanos():
    conn = getConnection()    
    sql = "SELECT id, nombre, celular, comuna_id FROM artesano"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    artesanos = cursor.fetchall()
    return artesanos

def get_hinchas():
    conn = getConnection()    
    sql = "SELECT id, nombre, celular, comuna_id, modo_transporte FROM hincha"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    hinchas = cursor.fetchall()
    return hinchas

  
def get_artesano_by_id(id):
    conn = getConnection()    
    sql = "SELECT id, nombre, celular, comuna_id, email, descripcion_artesania FROM artesano WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()
    artesano = cursor.fetchone()
    return artesano

def get_hincha_by_id(id):
    conn = getConnection()    
    sql = "SELECT id, nombre, email, celular, comuna_id, modo_transporte, comentarios FROM hincha WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    conn.commit()
    hincha = cursor.fetchone()
    return hincha
  
def get_comuna_id(comuna):
    conn = getConnection()    
    sql = "SELECT id FROM comuna WHERE nombre=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (comuna,))
    conn.commit()
    comuna_id = cursor.fetchone()
    return comuna_id  

def get_id_deporte(deporte):
    conn = getConnection()    
    sql = "SELECT id FROM deporte WHERE nombre=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (deporte,))
    conn.commit()
    id_deporte = cursor.fetchone()
    return id_deporte

  
def get_last_id_artesanos():
    conn = getConnection()
    sql = "SELECT id FROM artesano ORDER BY id DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    last_id = cursor.fetchone()
    return last_id

def get_last_id_hinchas():
    conn = getConnection()
    sql = "SELECT id FROM hincha ORDER BY id DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    last_id = cursor.fetchone()
    return last_id

  
def get_id_artesania(artesania):
    conn = getConnection()
    sql = "SELECT id FROM tipo_artesania WHERE nombre=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (artesania,))
    conn.commit()
    id_artesania = cursor.fetchone()
    return id_artesania
  
def get_id_foto():
    conn = getConnection()
    sql = "SELECT id FROM foto ORDER BY id DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    id_foto = cursor.fetchone()
    return id_foto
  
def get_fotos(id_artesano):
    conn = getConnection()
    sql = "SELECT ruta_archivo FROM foto WHERE artesano_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_artesano,))
    conn.commit()
    fotos = cursor.fetchall()
    return fotos
  
def get_artesanias_artesano(id_artesano):
    conn = getConnection()
    sql = "SELECT tipo_artesania_id FROM artesano_tipo WHERE artesano_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_artesano,))
    conn.commit()
    artesanias_artesano = cursor.fetchall()
    return artesanias_artesano

def get_deportes_hincha(id_hincha):
    conn = getConnection()
    sql = "SELECT deporte_id FROM hincha_deporte WHERE hincha_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_hincha,))
    conn.commit()
    deportes_hincha = cursor.fetchall()
    return deportes_hincha

  
def get_artesania_nombre(id_artesania):
    conn = getConnection()
    sql = "SELECT nombre FROM tipo_artesania WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_artesania,))
    conn.commit()
    artesania_nombre = cursor.fetchone()
    return artesania_nombre

def get_deporte_nombre(id_deporte):
    conn = getConnection()
    sql = "SELECT nombre FROM deporte WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_deporte,))
    conn.commit()
    deporte_nombre = cursor.fetchone()
    return deporte_nombre

def get_comuna_nombre(comuna_id):
    conn = getConnection()
    sql = "SELECT nombre FROM comuna WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (comuna_id,))
    conn.commit()
    comuna_nombre = cursor.fetchone()
    return comuna_nombre  

def get_region_nombre_by_comuna(comuna_id):
    conn = getConnection()
    sql = "SELECT region_id FROM comuna WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (comuna_id,))
    conn.commit()
    region_id = cursor.fetchone()
    sql = "SELECT nombre FROM region WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (region_id,))
    conn.commit()
    region_nombre = cursor.fetchone()
    return region_nombre
  
  
def validador_bbdd_artesano(nombre, email, celular, comuna_id):
    """
    Revisa si un artesano está en la tabla artesano.
    
    Retorna True si el artesano está en la tabla artesano, de lo contrario False.
    """
    conn = getConnection()
    sql = "SELECT id FROM artesano WHERE nombre=%s AND email=%s AND celular=%s AND comuna_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (nombre, email, celular, comuna_id))
    conn.commit()
    artesano = cursor.fetchone()
    return artesano is not None

def validador_bbdd_hincha(nombre, email, celular, comuna_id):
    """
    Revisa si un hincha está en la tabla hincha.
    
    Retorna True si el hincha está en la tabla hincha, de lo contrario False.
    
    """
    conn = getConnection()
    sql = "SELECT id FROM hincha WHERE nombre=%s AND email=%s AND celular=%s AND comuna_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (nombre, email, celular, comuna_id))
    conn.commit()
    hincha = cursor.fetchone()
    return hincha is not None
  
def insert_artesano_tipo(artesano_id, tipo_artesania_id):
  """
  Inserta un registro en la tabla artesano_tipo. La tabla posee columnas artesano_id(int)
  y tipo_artesania_id(int).
  """
  conn = getConnection()
  sql = "INSERT INTO artesano_tipo (artesano_id, tipo_artesania_id) VALUES (%s, %s)"
  cursor = conn.cursor()
  cursor.execute(sql, (artesano_id, tipo_artesania_id))
  conn.commit()
  conn.close()

def insert_artesano(id, comuna_id, descripcion_artesania, nombre, email, celular):
  """
  Inserta un registro en la tabla artesano. La tabla posee columnas id(int), comuna_id(int), 
  descripcion_artesania(varchar), nombre(varchar), email(varchar), celular(varchar).
  """
  conn = getConnection()
  sql = "INSERT INTO artesano (id, comuna_id, descripcion_artesania, nombre, email, celular) VALUES (%s, %s, %s, %s, %s, %s)"
  cursor = conn.cursor()
  cursor.execute(sql, (id, comuna_id, descripcion_artesania, nombre, email, celular))
  conn.commit()
  conn.close()
  
def insert_foto(id, ruta_archivo, nombre_archivo, artesano_id):
  """
  Inserta un registro en la tabla img. La tabla posee columnas id(int), ruta_archivo(varchar), 
  nombre_archivo(varchar), artesano_id(int).
  """
  conn = getConnection()
  sql = "INSERT INTO foto (id, ruta_archivo, nombre_archivo, artesano_id) VALUES (%s, %s, %s, %s)"
  cursor = conn.cursor()
  cursor.execute(sql, (id, ruta_archivo, nombre_archivo, artesano_id))
  conn.commit()
  conn.close()
  
  
def insert_hincha(id, comuna_id, transporte, nombre, email, celular, comentario):
    """
    Inserta un hincha en la tabla hincha.
    """
    conn = getConnection()
    sql = "INSERT INTO hincha (id, comuna_id, modo_transporte, nombre, email, celular, comentarios) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (id, comuna_id, transporte, nombre, email, celular, comentario))
    conn.commit()
    conn.close()
    
def insert_hincha_deporte(hincha_id, deporte_id):
    """
    Inserta el id del hincha y el id del deporte en la tabla hincha_deporte.
    """
    conn = getConnection()
    sql = "INSERT INTO hincha_deporte (hincha_id, deporte_id) VALUES (%s, %s)"
    cursor = conn.cursor()
    cursor.execute(sql, (hincha_id, deporte_id))
    conn.commit()
    conn.close()
    
    
def get_artesanos_stats():
    """
    Se accede a la tabla artesano_tipo y se obtiene la cantidad de artesanos por tipo de artesanía.

    """
    conn = getConnection()
    sql = "SELECT tipo_artesania_id, COUNT(*) FROM artesano_tipo GROUP BY tipo_artesania_id"
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    stats = cursor.fetchall()
    return stats

def get_artesanos_stats_by_artesania(id_artesania):
    """
    retorna la cantidad de artesanos por artesanía.
    """
    conn = getConnection()
    sql = "SELECT COUNT(*) FROM artesano_tipo WHERE tipo_artesania_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_artesania,))
    conn.commit()
    stats = cursor.fetchone()
    return stats

def get_hinchas_stats_by_deporte(id_deporte):
    """
    retorna la cantidad de hinchas por deporte.
    """
    conn = getConnection()
    sql = "SELECT COUNT(*) FROM hincha_deporte WHERE deporte_id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_deporte,))
    conn.commit()
    stats = cursor.fetchone()
    return stats

  

def create_register_without_image(id_artesano,
                                  nombre,
                                  email,
                                  celular,
                                  descripcion_artesania,
                                  comuna_id,
                                  tipo_artesania_id):
  
  # llamamos a la función insert_artesano para insertar un registro en la tabla artesano
  insert_artesano(id_artesano, comuna_id, descripcion_artesania, nombre, email, celular)
  
  # llamamos a la función insert_artesano_tipo para insertar un registro en la tabla artesano_tipo
  insert_artesano_tipo(id_artesano, tipo_artesania_id)
  
  
  
