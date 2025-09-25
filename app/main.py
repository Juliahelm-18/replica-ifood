from fastapi import FastAPI
from app.routers import restaurante_router

app = FastAPI(title="Réplica do iFood!")

app.include_router(restaurante_router, prefix="/restaurants", tags=["Restaurantes"])
