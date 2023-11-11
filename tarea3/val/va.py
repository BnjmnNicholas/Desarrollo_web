import re
import filetype
import hashlib
from werkzeug.utils import secure_filename
import bleach

# ------------------------------------------------------------------------------------------
                                        # FN Aux Val

def validador_mail(mail):
    """
    Valida si una dirección de correo electrónico tiene el formato regex.

    Args:
        mail (str): La dirección de correo electrónico.

    Returns:
        bool: True si el formato de correo es válido, de lo contrario False.
    """
    regex = r'^\S+@\S+\.\S+$'
    return re.match(regex, bleach.clean(mail)) is not None

def validador_nombre(nombre):
    """
    Valida si un nombre dado cumple con condiciones.

    Args:
        nombre (str): El nombre a ser validado.

    Returns:
        bool: True si el nombre cumple con las condiciones, de lo contrario False
    """
    nombre = bleach.clean(nombre)
    
    return nombre and 3 < len(nombre) < 80

def validador_artesanias(artesania_1, artesania_2, artesania_3):
    """
    Valida si al menos una de las tres artesanías dadas está seleccionada.

    Args:
        artesania_1 (bool): Estado de la primera artesanía.
        artesania_2 (bool): Estado de la segunda artesanía.
        artesania_3 (bool): Estado de la tercera artesanía.

    Returns:
        bool: True si al menos una artesanía está seleccionada, de lo contrario False.
    """
    
    return artesania_1 or artesania_2 or artesania_3


def validador_region(region):
    """
    Valida si una región está seleccionada.

    Args:
        region (str): La región seleccionada.

    Returns:
        bool: True si una región está seleccionada, de lo contrario False.
    """
    return bool(region)

def validador_comuna(comuna):
    """
    Valida si una comuna está seleccionada.

    Args:
        comuna (str): La comuna seleccionada.

    Returns:
        bool: True si una comuna está seleccionada, de lo contrario False.
    """
    return bool(comuna)


def validador_celular(celular):
    """
    Valida si un número de teléfono dado sigue un formato específico
    (iniciar con '+' y debe tener entre 9  y 11 numeros).

    Args:
        celular (str): El número de teléfono a ser validado.

    Returns:
        bool: True si el número de teléfono sigue el formato especificado, de lo contrario False.
    """
    
    celular = bleach.clean(celular)
    return len(celular) == 0 or re.match(r'^(\+)?(\d{9,11})$', celular) is not None


def validador_imagen(imagen):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}

    # check if a file was submitted
    if imagen is None:
        return False

    # check if the browser submitted an empty file
    if imagen.filename == "":
        return False
    
    # check file extension
    ftype_guess = filetype.guess(imagen)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    # check mimetype
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True


def validador_descripcion(descripcion):
    """
    Valida si una descripción dada cumple con condiciones, puede ser vacia.

    Args:
        descripcion (str): La descripción a ser validada.

    Returns:
        bool: True si la descripción cumple con las condiciones, de lo contrario False.
    """
    if descripcion is None:
        return True
    return len(descripcion) < 500
    
    
    


def new_name(img, filename, id):
    secure_name = secure_filename(filename)
    hashed_name = str(id) + '_' + hashlib.sha256(secure_name.encode("utf-8")).hexdigest()
    _extension = filetype.guess(img).extension
    img_filename = f"{hashed_name}.{_extension}"
    return img_filename