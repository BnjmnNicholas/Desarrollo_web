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