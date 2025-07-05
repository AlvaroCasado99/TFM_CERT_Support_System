# This is the point of entry to my api
from fastapi import FastAPI
from app.api.routes import analysis, report_router
from app.db.db import init_db


app = FastAPI()

# Acciones que deben realizarse al lanzar la API
@app.on_event("startup")
async def app_init():
    await init_db()

# Routers
app.include_router(analysis.router, prefix='/analyse')
app.include_router(report_router.router, prefix='/report')

# Tensting endpoint
@app.get("/test") 
def test():
    return {
            "message": "La API esta funcionando."
            }

