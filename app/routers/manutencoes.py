from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db

from app.models.manutencao import Manutencao

router = APIRouter(prefix="/api/manutencao", tags=["Manutenções"])

@router.get("/ativas")
def listar_manutencoes_ativas(db: Session = Depends(get_db)):
    manutencoes = db.query(Manutencao).filter(Manutencao.data_conclusao == None).all()
    return manutencoes