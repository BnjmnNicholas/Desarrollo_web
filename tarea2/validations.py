import re
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
    return re.match(regex, mail) is not None

def validador_nombre(nombre):
    """
    Valida si un nombre dado cumple con condiciones.

    Args:
        nombre (str): El nombre a ser validado.

    Returns:
        bool: True si el nombre cumple con las condiciones, de lo contrario False.
    """
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

def validador_transporte(transporte):
    """
    Valida si se ha seleccionado un método de transporte.

    Args:
        transporte (str): El método de transporte seleccionado.

    Returns:
        bool: True si se ha seleccionado un método de transporte, de lo contrario False.
    """
    return bool(transporte)

def validador_celular(celular):
    """
    Valida si un número de teléfono dado sigue un formato específico
    (iniciar con '+' y debe tener entre 9  y 11 numeros).

    Args:
        celular (str): El número de teléfono a ser validado.

    Returns:
        bool: True si el número de teléfono sigue el formato especificado, de lo contrario False.
    """
    return len(celular) == 0 or re.match(r'^(\+)?(\d{9,11})$', celular) is not None

def validador_imagen(imagen):
    """
    Valida si una ruta de imagen dada es de un formato de imagen permitido.

    Args:
        imagen (str): La ruta de la imagen a ser validada.

    Returns:
        bool: True si la imagen tiene una extensión de archivo válida, de lo contrario False.
    """
    return imagen and (".jpg" in imagen or ".png" in imagen or ".jpeg" in imagen)

