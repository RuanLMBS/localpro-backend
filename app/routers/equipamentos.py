# app/routers/equipamentos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.equipamento import Equipamento
from app.schemas.equipamento import EquipamentoCreate, EquipamentoResponse

router = APIRouter(prefix="/api/equipamentos", tags=["Equipamentos"])

@router.post("/", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_equipamento(equip_in: EquipamentoCreate, db: Session = Depends(get_db)):
    equip_existente = db.query(Equipamento).filter(Equipamento.numero_patrimonio == equip_in.numero_patrimonio).first()
    if equip_existente:
        raise HTTPException(status_code=400, detail="Número de patrimônio já cadastrado.")
    
    novo_equipamento = Equipamento(**equip_in.model_dump())

    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)

    return novo_equipamento

@router.get("/", response_model=List[EquipamentoResponse])
def listar_equipamentos(db: Session = Depends(get_db)):
    return db.query(Equipamento).all()