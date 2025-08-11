""" Funciones para analizar la entrada de mensajes de sminshing """

import pandas as pd

from typing import Dict, Any
from web.validation.validation import validate_no_html_tags
from web.validation.file_validator import spread_sheet_validator
from web.exceptions.file_exceptions import ValidationError
from web.utils.constants import FILE_MESSAGE_COLUMN

# Lógica para analizar mensajes únicos de text
def process_single_message(msg: str) -> str:
    valid = validate_no_html_tags(msg)

    if valid:
        return {'ok': True}
    else:
        return {
                'ok': False,
                'error': "Este mensaje contiene código HTML por lo que no puede ser procesado."
            }


# lógica para analizar mensajes hojas de cálculo con mensajes dentro
def process_multiple_messages(file) -> Dict[str, Any]:
    print(type(file))
    # Validar que el archivo cumple con los requisitos
    try:
        validated = spread_sheet_validator(file, columns=['TEXT'])
    except ValidationError as e:
        return {
                'ok': False,
                'error': str(e)
            }

    # Filtrar mensajes que tengan código html
    warning=""
    filter_mask = validated[FILE_MESSAGE_COLUMN].apply(validate_no_html_tags)
    filtered = validated[filter_mask]

    # Avisar si se han eliminado mensajes
    if not len(validated) == len(filtered):
        warning="Se han encontrado y eliminado mensajes con código HTML"

    return {
            'ok': True,
            'warn': warning,
            'result': filtered
        }
