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


def validador_deportes(deporte_1, deporte_2, deporte_3):
    """
    Valida si al menos uno de los tres deportes de interes esta seleccionado.
    
    Args:
        deporte_1 (bool): Estado del primer deporte.
        deporte_2 (bool): Estado del segundo deporte.
        deporte_3 (bool): Estado del tercer deporte.
        
    Returns:
        bool: True si al menos un deporte esta seleccionado, de lo contrario False.
    """
        
    return deporte_1 or deporte_2 or deporte_3


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

def validador_transporte(transporte):
    """
    Valida si un transporte está seleccionado.

    Args:
        transporte (str): El transporte seleccionado.

    Returns:
        bool: True si un transporte está seleccionado, de lo contrario False.
    """
    return bool(transporte)



def validador_comentario(comentario):
    """
    Valida si una descripción dada cumple con condiciones, puede ser vacia.

    Args:
        descripcion (str): La descripción a ser validada.

    Returns:
        bool: True si la descripción cumple con las condiciones, de lo contrario False.
    """
    if comentario is None:
        return True
    return len(comentario) < 80
    
    
    