from datetime import datetime 
from zoneinfo import ZoneInfo

def get_current_timestamp(dateformat="%d-%m-%Y %H:%M:%S %Z"):
    zone = ZoneInfo("Europe/Madrid")
    current = datetime.now(tz=zone)
    return current.strftime(dateformat)
