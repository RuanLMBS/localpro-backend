from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.database.database import get_db

from app.models.manutencao import Manutencao
from app.schemas.manutencao import ManutencaoResponse

from app.models.equipamento import Equipamento, StatusEquipamento

from app.services.locacao_service import concluir_manutencao_service

router = APIRouter(prefix="/api/manutencao", tags=["Manutenções"])

@router.get("/ativas", response_model=List[ManutencaoResponse])
def listar_manutencoes_ativas(db: Session = Depends(get_db)):
    manutencoes = db.query(Manutencao).filter(Manutencao.data_conclusao == None).all()
    return manutencoes

@router.put("/{id}/concluir", status_code=status.HTTP_200_OK)
def concluir_manutencao(id: int, db: Session = Depends(get_db)):
    resultado = concluir_manutencao_service(manutencao_id=id, db=db)

    return resultado