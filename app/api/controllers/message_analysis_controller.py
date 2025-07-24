import httpx
import asyncio

from app.models.issue import Issue
from app.models.smishing import Smishing, SmishingProjectionFAISS

from beanie import PydanticObjectId



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
    if isinstance(msg, list):
        # Loop entre cada mensaje
        results = list()
        for m in msg:
            msg_info = await _analyse_text(m)
            results.append(msg_info)

        return {
                "results": results
                }

    else:
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
async def _normal_post_request(url, data, timeout=5.0):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, timeout=timeout)
            response.raise_for_status() # Verificar que no sea un error 4xx/5xx

            return response.json()["result"]
    except httpx.ConnectError:
        print("[ERROR]: No se pudo conectar con el servicio de HTML")
    except httpx.ReadTimeout:
        print("[ERROR]: No se pudo conectar con el servicio HTML, se excedió el tiempo de espera")
    except httpx.HTTPStatusError as e:
        print(f"[ERROR]: El microservicio HTML respondió con el error HTTP: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"[ERROR]: Error general en la peticion: {e}")



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
        _limited_post_request("http://localhost:8001/check", {"msg": msg}),
        _limited_post_request("http://localhost:8001/entity", {"msg": msg}),
        _limited_post_request("http://localhost:8001/embedding", {"msg": msg})
    )

    # Conocer el tipo de smishing
    issue.flavour = preds

    # Buscar entidades en el mensaje
    issue.entity = entities["org"][0]

    # Obtener los embeddings
    issue.embeddings = embeds["embeddings"]
    issue.norm_embeddings = embeds["norm_embeddings"]

    # Identificar URL, MAIL, PHONE
    issue.url = entities["url"]
    issue.mail = entities["email"]
    issue.phone = ""

    # Obtener código HTML de la URL
    print("Voy a buscar el HTML ")
    if issue.url != "":
        issue.html = await _normal_post_request(
                url="http://localhost:8002/url", 
                data={"url": issue.url}, 
                timeout=5.0
            )

    # Obtener (si existe campaña asociada)
    print("Voy a buscar su campaña")
    issue.campaign = await _normal_post_request(
            url="http://localhost:8003/campaign", 
            data={"embedding": issue.norm_embeddings}, 
            timeout=5.0
        )
    
    # Actualizar el índice con los mensajes
    print("Voy a actualizar el índice")
    await _normal_post_request(
            url="http://localhost:8003/update", 
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


    return issue.to_dict()

