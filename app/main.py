from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base

from app.routers import locacoes, clientes, equipamentos, auth, manutencoes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LocalPro API",
    description="Backend do LocalPro",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(locacoes.router)
app.include_router(clientes.router)
app.include_router(equipamentos.router)
app.include_router(auth.router)
app.include_router(manutencoes.router)

@app.get("/")
def health_check():
    return {"mensagem": "No ar!"}