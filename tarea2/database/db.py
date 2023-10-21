import pymysql


def getConnection():
  conn = pymysql.connect(
    db='tarea2',
    user='root',
    passwd='nicholas6308',
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
  
def get_comuna_id(comuna):
    conn = getConnection()    
    sql = "SELECT id FROM comuna WHERE nombre=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (comuna,))
    conn.commit()
    comuna_id = cursor.fetchone()
    return comuna_id  
  
def get_last_id_artesanos():
    conn = getConnection()
    sql = "SELECT id FROM artesano ORDER BY id DESC LIMIT 1"
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
  
def get_artesania_nombre(id_artesania):
    conn = getConnection()
    sql = "SELECT nombre FROM tipo_artesania WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (id_artesania,))
    conn.commit()
    artesania_nombre = cursor.fetchone()
    return artesania_nombre
  
  
def get_comuna_nombre(comuna_id):
    conn = getConnection()
    sql = "SELECT nombre FROM comuna WHERE id=%s"
    cursor = conn.cursor()
    cursor.execute(sql, (comuna_id,))
    conn.commit()
    comuna_nombre = cursor.fetchone()
    return comuna_nombre  
  
  
  
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
  
  
