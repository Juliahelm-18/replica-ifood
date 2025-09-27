from fastapi import FastAPI
from app.routers.restaurante_router import router as restaurante_router

app = FastAPI(title="Réplica do iFood!")

app.include_router(restaurante_router)

@app.get("/")
def raiz():
    return {"mensagem": "API rodando! 🚀"}
