from fastapi import FastAPI
from app.database.database import engine, Base

from app.routers import locacoes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LocalPro API",
    description="Backend do LocalPro",
    version="1.0.0"
)

app.include_router(locacoes.router)

@app.get("/")
def read_root():
    return {"mensagem": "API LocaPro online e banco de dados sincronizado!"}