import httpx
import asyncio
import logging

from models.issue import Issue
from models.smishing import Smishing, SmishingProjectionFAISS

from beanie import PydanticObjectId


# Obtener el logger
logger = logging.getLogger("API")



"""
    DELETE:
    Para probar como funciona beanie
"""
async def db_test():
    results = await Smishing.find({}).project(SmishingProjectionFAISS).to_list()
    

    for idx, doc in enumerate(results):
        print(results[idx].id)
    return {
            "results": results
            }


"""
    Como las requests pueden contener uno o más mensajes, esta función maneja ambas lógicas
    y delega el proceso de análisis a la función interna: _analyse_text.
"""
async def advanced_text_analysis(msg):
    logger.info("Iniciando procesamiento de datos...")
    if isinstance(msg, list):
        print("Voy a procesar una lista")
        # Loop entre cada mensaje
        results = list()
        for m in msg:
            logger.info(f"MSG: {m}\n")
            msg_info = await _analyse_text(m)
            results.append(msg_info)
            logger.info("--> Terminado de procesar este mensaje")

        return results

    else:
        print("Voy a procesar un mensaje único.")
        return await _analyse_text(msg)


"""
    Función interna: NO IMPORTAR
    Controla la concurrencia para peticiones con asyncio gather
"""
semaforo = asyncio.Semaphore(5)
async def _limited_post_request(url, data, timeout=30.0):
    async with semaforo:
        return await _normal_post_request(url, data, timeout)
        

"""
    Función interna: NO IMPORTA
    Contiene la lógica para hacer peticiones a microservicios de forma no concurrente
"""
async def _normal_post_request(url, data, timeout=10.0):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=timeout)
            response.raise_for_status() # Verificar que no sea un error 4xx/5xx
            return response.json()["result"]
    except httpx.ConnectError:
        print("[ERROR]: No se pudo conectar con el servicio.")
    except httpx.ReadTimeout:
        print("[ERROR]: No se pudo conectar con el servicio, se excedió el tiempo de espera")
    except httpx.HTTPStatusError as e:
        print(f"[ERROR]: El microservicio respondió con el error HTTP: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"[ERROR]: Error general en la peticion: {e}")
    except httpx.ReadTimeout as e:
        print(f"[ERROR]: Se excedió el tiempo para la url: {url}")
    except Exception as e:
        print(f"[ERROR]: Ha ocurrido un error inesperado: {e}")



"""
    Función interna: NO IMPORTAR

    Extrae los elementos de un mensaje de posible smishing, los guarda en la base de datos,
    los organiza y devuelve al usuario. Para el análisis se hacen peticiones a APIs de 
    microsercivios que contienen los modelos que extraen la información. Otros datos son
    extraidos localmente.
"""
async def _analyse_text(msg):
    issue = Issue()

    issue.msg = msg

    # Paralelización de las peticiones a los contenedores
    preds, entities, embeds = await asyncio.gather(
        _limited_post_request("http://ms1:8000/check", {"msg": msg}),
        _limited_post_request("http://ms1:8000/entity", {"msg": msg}),
        _limited_post_request("http://ms1:8000/embedding", {"msg": msg})
    )

    # Conocer el tipo de smishing
    issue.flavour = preds['7c']
    issue.flavour_13c = preds['13c']

    # Buscar entidades en el mensaje
    if entities["org"]:
        issue.entity = entities["org"][0]

    # Obtener los embeddings
    issue.embeddings = embeds["embeddings"]
    issue.norm_embeddings = embeds["norm_embeddings"]

    # Identificar URL, MAIL, PHONE
    issue.url = entities["url"]
    issue.mail = entities["email"]
    issue.phone = ""

    # Obtener código HTML de la URL
    if issue.url != "":
        html = await _normal_post_request(
                url="http://ms2:8000/url", 
                data={"url": issue.url}, 
                timeout=5.0
            )
        print(f"HTML: {type(html)}")
        issue.html = html

    # Obtener (si existe) campaña asociada
    issue.campaign = await _normal_post_request(
            url="http://ms3:8000/campaign", 
            data={"embedding": issue.norm_embeddings}, 
            timeout=10.0
        )
    
    # Actualizar el índice con los mensajes
    await _normal_post_request(
            url="http://ms3:8000/update", 
            data={
                "norm_embeddings": issue.norm_embeddings,
                "campaign": issue.campaign
                }, 
            timeout=5.0
        )

    # Subir a la base de datos la ISSUE
    message = Smishing(
            msg = issue.msg,
            flavour = issue.flavour,
            flavour_13c = issue.flavour_13c,
            entity = issue.entity,
            url = issue.url,
            mail = issue.mail,
            phone = issue.phone,
            html = issue.html,
            embeddings = issue.embeddings,
            norm_embeddings = issue.norm_embeddings,
            campaign = issue.campaign

            )
    await Smishing.insert_one(message)

    
    logger.info("Saliendo del analizador...")
    return issue.to_dict()

