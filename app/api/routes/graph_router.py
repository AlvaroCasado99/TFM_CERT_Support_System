import pandas as pd

from fastapi import APIRouter, HTTPException, status
from app.models.requests import GraphRequest
from app.models.smishing import Smishing, SmishingProjectionGraphCategory, SmishingProjectionGraphOrganizationCategory

# Router
router = APIRouter()




# Endpoint de prueba para este router
@router.get("/test")
def get_analysis_test():
    return {
            "message": "Router /graph funciona!"
            }

# Endpoint para obtener los datos usados en un grafico PIE de categorias
@router.post("/msg_categories")
async def graph_msg_category(req: GraphRequest):
    data = await Smishing.find(
            {
                "created_at": {
                    "$gte": req.start,
                    "$lt": req.end
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


# Crear columna de agrupación temporal
def _group_data_by_time_interval(df: pd.DataFrame, interval: str) -> pd.DataFrame:
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


# Endpoint para obetener datos usados en un gráfico STACKED BAR. El gráfico cuenta con 
# categorías agrupadas por plazos de tiempo.
@router.post("/stack_bar_time_categories")
async def graph_stack_bar_time_categories(req: GraphRequest):
    data = await Smishing.find({
        "created_at": {
            "$gte": req.start,
            "$lt": req.end
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
    df = _group_data_by_time_interval(df, req.interval)

    # Agrupar y contar
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


# Endpoint para obetener datos usados en un gráfico STACKED HORIZONTAL BAR.
# El gráfico muestra las empresas más comunes y en que tipo de mensajes aparecen.
@router.post("/categories_organizations")
async def graph_stack_hbar_categories_organizations(req: GraphRequest):
    data = await Smishing.find({
        "created_at": {
            "$gte": req.start,
            "$lt": req.end
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

    print(grouped)

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


