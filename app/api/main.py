# This is the point of entry to my api
from fastapi import FastAPI
from app.api.routes import analysis, report_router, user_router, graph_router
from app.db.db import init_db
from app.logger_config.setup_logger import setup_logger


app = FastAPI()

# Lanzar el logger
logger = setup_logger("API", "api.log")
logger.info("API arrancando")

# Acciones que deben realizarse al lanzar la API
@app.on_event("startup")
async def app_init():
    await init_db()

# Routers
app.include_router(analysis.router, prefix='/analyse')
app.include_router(report_router.router, prefix='/report')
app.include_router(user_router.router, prefix='/user')
app.include_router(graph_router.router, prefix='/graph')

# Tensting endpoint
@app.get("/test") 
def test():
    return {
            "message": "La API esta funcionando."
            }

