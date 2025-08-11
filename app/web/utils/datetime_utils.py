from datetime import datetime, timedelta 
from zoneinfo import ZoneInfo

def get_current_timestamp(dateformat="%d-%m-%Y %H:%M:%S %Z"):
    zone = ZoneInfo("Europe/Madrid")
    current = datetime.now(tz=zone)
    return current.strftime(dateformat)


# Devuleve un rango de fechas segun las opciones disponibles
def obtener_rango_fechas(rango: str) -> tuple[datetime, datetime]:
    ahora = datetime.now()

    if rango == "Hoy":
        inicio = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    elif rango == "7 días":
        inicio = (ahora - timedelta(days=6)).replace(hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Mes":
        inicio = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Año":
        inicio = ahora.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    elif rango == "Todo":
        inicio = datetime(2000, 1, 1)
    else:
        raise ValueError(f"Rango no reconocido: {rango}")

    fin = ahora
    return inicio, fin
