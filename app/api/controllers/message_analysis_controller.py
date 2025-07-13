import httpx
import asyncio

from app.models.issue import Issue
from app.models.smishing import Smishing


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

    Extrae los elementos de un mensaje de posible smishing, los guarda en la base de datos,
    los organiza y devuelve al usuario. Para el análisis se hacen peticiones a APIs de 
    microsercivios que contienen los modelos que extraen la información. Otros datos son
    extraidos localmente.
"""
async def _analyse_text(msg):
    issue = Issue()

    issue.msg = msg

    # Paralelización de las peticiones a los contenedores
    async with httpx.AsyncClient() as client:
        r1, r2, r3, r4, r5 = await asyncio.gather(
                client.post("http://localhost:8001/check", json={"msg": msg}),
                client.post("http://localhost:8001/entity", json={"msg": msg}),
                client.post("http://localhost:8001/embedding", json={"msg": msg}),
                client.post("http://localhost:8002/html", json={"msg": msg}),
                client.post("http://localhost:8003/campaign", json={"msg": msg}),
        )

    r1 = r1.json()["predictions"]
    r2 = r2.json()["entity"]
    r3 = r3.json()
    r4 = r4.json()["html"]
    r5 = r5.json()["campaign"]

    # Conocer el tipo de smishing
    issue.flavour = r1

    # Buscar entidades en el mensaje
    issue.entity = r2

    # Obtener los embeddings
    issue.embedding = r3["embedding"]
    issue.norm_embedding = r3["norm_embedding"]

    # Identificar URL, MAIL, PHONE
    issue.url = "http://URL_de_prueba.com"
    issue.mail = "mqil@example.com"
    issue.phone = "987-54-12-54"

    # Obtener código HTML de la URL
    if issue.url:
        issue.html = r4

    # Obtener (si existe campaña asociada)
    issue.campaign = r5

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


