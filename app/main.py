from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base

from app.routers import locacoes, clientes, equipamentos, auth, manutencoes

from app.config.settings import DOMAIN_URL

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LocalPro API",
    description="Backend do LocalPro",
    version="1.0.0"
)

allowed_origins = [
    "http://localhost:5173"
]

if DOMAIN_URL:
    allowed_origins.append(DOMAIN_URL)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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