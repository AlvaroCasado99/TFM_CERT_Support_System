""" Aquí van validadores de archivos"""

import pandas as pd
import web.validation.validation as val
from web.exceptions.file_exceptions import ValidationError, FileExtensionError, FileSizeError, ContentError

def spread_sheet_validator(file, columns: list, max_rows: int = 150, max_size: int = 20971520) -> pd.DataFrame:
    try:
        # Validar extension de archivo
        val.validate_spread_sheet_extension(file)

        # Validar tamaño de archivo
        val.validate_file_size(file, max_size)

        # Convertir a dataframe para seguir validando
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)

        # Validar columnas requeridas
        val.validate_dataframe_columns(df, columns)

        # Validar numero de filas
        val.validate_dataframe_rows(df, max_rows)

        return df

    except (FileExtensionError, FileSizeError, ContentError) as e:
        raise ValidationError(f"Este archivo no es válido. {e}")
