# This is the point of entry to my api

from fastapi import FastAPI
from app.api.routes import analysis

app = FastAPI()

# Routers
app.include_router(analysis.router, prefix='/analyse')

# Tensting endpoint
@app.get("/test") 
def test():
    return {
            "message": "La API esta funcionando."
            }

