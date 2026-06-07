from fastapi import FastAPI
from app.database.database import engine, Base

from app.routers import locacoes, clientes, equipamentos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LocalPro API",
    description="Backend do LocalPro",
    version="1.0.0"
)

app.include_router(locacoes.router)
app.include_router(clientes.router)
app.include_router(equipamentos.router)

@app.get("/")
def health_check():
    return {"mensagem": "No ar!"}