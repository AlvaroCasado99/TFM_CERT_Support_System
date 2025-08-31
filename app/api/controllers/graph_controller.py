import pandas as pd

#from fastapi import APIRouter, HTTPException, status
#from app.models.requests import GraphRequest
from models.smishing import Smishing, SmishingProjectionGraphCategory, SmishingProjectionGraphOrganizationCategory, SmishingProjectionGraphMessages

#==============================
#----- FUNCIONES LOCALES ------
#==============================

# Crear columna de agrupación temporal
def _group_data_by_time_interval(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    # Normaliza timestamps a UTC y hazlos "naive" (sin tz)
    df['created_at'] = pd.to_datetime(df['created_at'], utc=True, errors='coerce').dt.tz_localize(None)

    if interval == 'D':
        df['time_group'] = df['created_at'].dt.date
    elif interval == 'H':
        df['time_group'] = df['created_at'].dt.floor('h')
    elif interval == 'W':
        df['time_group'] = df['created_at'].dt.to_period('W').dt.start_time
    elif interval == 'M':
        df['time_group'] = df['created_at'].dt.to_period('M').dt.start_time
    else:
        raise ValueError("El valor de intervalo no es válido")

    return df


#==============================
#---- FUNCIONES IMPORTABLES----
#==============================

"""
    Devuelve los datos necesarios, usados en 
"""
async def get_graph_message_category_data(start, end) -> dict:
    # Obtener los datos necesarios
    data = await Smishing.find(
            {
                "created_at": {
                    "$gte": start,
                    "$lt": end
                }
            }
    ).project(SmishingProjectionGraphCategory).to_list()

    # Convertir objetos beanie en un diccionario
    data = [obj.model_dump() for obj in data]

    # Comprobar que no esté vacio
    if not data:
        return None

    counts = pd.DataFrame(data)["flavour"].value_counts()
    df = counts.reset_index()
    df.columns = ['labels', 'counts']

    return {
                'labels': df['labels'].to_list(),
                'counts': df['counts'].to_list()
            }


"""
"""
async def get_stacked_bar_time_categories_data(start, end, interval) -> dict:
    # Obtener Datos
    data = await Smishing.find({
        "created_at": {
            "$gte": start,
            "$lt": end
        }
    }).project(SmishingProjectionGraphCategory).to_list()

    # Convertir objetos beanie en un diccionario
    data = [obj.model_dump() for obj in data]

    # Comprobar que no esté vacío
    if not data:
        return None
    
    # Convertir los ISODates de Mongo en objetos datetime
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df = _group_data_by_time_interval(df, interval)

    # Agrupar por tipo y tiempo, calcula la cantidad de cada tipo, rellena con 0 los periodos sin mensaje
    grouped = df.groupby(['time_group', 'flavour']).size().unstack(fill_value=0).T
    
    # Obtener y serializar los timestamps
    columns = grouped.columns.tolist()
    timestamps = [ts.strftime("%d-%m-%Y %H:%M:%S") for ts in columns]

    # Crear diccionario de categorias y valores
    values = dict()
    rows = grouped.index.tolist()
    for idx, row_data in grouped.iterrows():
        values[idx] = row_data.tolist()

    return {
            "timestamps": timestamps,
            "categories": rows,
            "values": values
        }


"""
"""
async def get_stacked_barh_categories_organizarions_data(start, end) -> dict:
    data = await Smishing.find({
        "created_at": {
            "$gte": start,
            "$lt": end
        }
    }).project(SmishingProjectionGraphOrganizationCategory).to_list()

    # Convertir objetos beanie en un diccionario
    data = [obj.model_dump() for obj in data if not obj.entity==""]

    # Comprobar que no esté vacío
    if not data:
        return None
    
    df = pd.DataFrame(data)

    # Agrupar y contar
    grouped = df.groupby(['entity', 'flavour']).size().unstack(fill_value=0).T
    grouped = grouped.loc[grouped.sum(axis=1).nlargest(10).index]

    # Obtener y serializar los timestamps
    orgs = grouped.columns.tolist()

    # Crear diccionario de categorias y valores
    values = dict()
    rows = grouped.index.tolist()
    for idx, row_data in grouped.iterrows():
        values[idx] = row_data.tolist()

    return{
            "organizations": orgs,
            "categories": rows,
            "values": values
        }


"""
"""
async def get_graph_messages_data(start, end) -> dict:
    data = await Smishing.find({
        "created_at": {
            "$gte": start,
            "$lt": end
        }
    }).project(SmishingProjectionGraphMessages).to_list()

    # Convertir objetos beanie en un diccionario
    data = [obj.model_dump() for obj in data]

    # Comprobar que no esté vacío
    if not data:
        return None

    # Juntar todos los mensajes en una lista
    texts = [obj['msg'] for obj in data if 'msg' in obj]

    return {
            "msg_list": texts,
            "joined": " ".join(texts)
            }
