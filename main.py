from fastapi import FastAPI
from routers import tickets

app = FastAPI(title="APPGafister")

# Incluir rutas desde el archivo tickets.py
app.include_router(tickets.router)

@app.get("/")
async def root():
    return {"message": "Servidor APPGafister funcionando correctamente"}
