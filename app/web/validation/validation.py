""" Contiene funciones útiles para validar archivos, entradas..."""

import pandas as pd

from web.utils.tag_detector import tag_detector
from web.utils.general_utils import is_sublist
from web.exceptions.file_exceptions import FileExtensionError, FileSizeError, ContentError

def validate_spread_sheet_extension(file) -> None:
    if not file.name.endswith('.csv') and not file.name.endswith('.xlsx'):
        raise FileExtensionError("La extensión no coincide con con la de una hoja de cálculo.")

def validate_file_size(file, max_size: int) -> None:
    if not file.size <= max_size:
        raise FileSizeError("El archivo es demasiado grande.")

def validate_dataframe_rows(df: pd.DataFrame, max_rows: int) -> None:
    if len(df) > max_rows:
        raise ContentError(f"El archivo supera el máximo de {max_rows} columnas")

def validate_dataframe_columns(df: pd.DataFrame, columns: list) -> None:
    if not is_sublist(columns, df.columns):
        raise ContentError(f"Las columnas siguientes deben estar presentes: {' '.join(columns)}")

def validate_no_html_tags(text: str) -> bool:
    return not tag_detector.detect_html(text)
