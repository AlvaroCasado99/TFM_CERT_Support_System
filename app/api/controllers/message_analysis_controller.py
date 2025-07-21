import httpx
import asyncio

from app.models.issue import Issue
from app.models.smishing import Smishing, SmishingProjectionFAISS



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
async def _limited_request(url, data):
    async with semaforo:
        async with httpx.AsyncClient(timeout=30.0) as client:
            return await client.post(url, json=data)


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
    r1, r2, r3 = await asyncio.gather(
        _limited_request("http://localhost:8001/check", {"msg": msg}),
        _limited_request("http://localhost:8001/entity", {"msg": msg}),
        _limited_request("http://localhost:8001/embedding", {"msg": msg})
    )

    print(r2)

    r1 = r1.json()["predictions"]
    r2 = r2.json()
    r3 = r3.json()

    # Conocer el tipo de smishing
    issue.flavour = r1

    # Buscar entidades en el mensaje
    issue.entity = r2["org"][0]

    # Obtener los embeddings
    issue.embeddings = r3["embeddings"]
    issue.norm_embeddings = r3["norm_embeddings"]

    # Identificar URL, MAIL, PHONE
    issue.url = r2["url"]
    issue.mail = r2["email"]
    issue.phone = ""

    # Obtener código HTML de la URL
    print("Voy a buscar el HTML ")
    if issue.url != "":
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:8002/url", json={"url": issue.url})
        response = response.json()["html"]
        issue.html = response

    # Obtener (si existe campaña asociada)
    print("Voy a buscar su campaña")
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8003/campaign", json={"embedding": issue.norm_embeddings})

    print(response)
    response = response.json()["campaign"]
    issue.campaign = response

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


