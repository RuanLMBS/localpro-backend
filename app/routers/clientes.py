# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse

from sqlalchemy import func
from app.models.locacao import Locacao

from app.routers.auth import ler_usuario_atual

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(cliente_in: ClienteCreate, db: Session = Depends(get_db), current_user = Depends(ler_usuario_atual)):
    cliente_existente = db.query(Cliente).filter(
        Cliente.cnpj == cliente_in.cnpj,
        Cliente.usuario_id == current_user.id
    ).first()

    if cliente_existente:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")
    
    novo_cliente = Cliente(**cliente_in.model_dump(), usuario_id=current_user.id)

    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return novo_cliente

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), current_user = Depends(ler_usuario_atual)):
    resultados = db.query(
        Cliente,
        func.count(Locacao.id).filter(Locacao.data_devolucao_real == None).label("total")
    ).outerjoin(
        Locacao, Locacao.cliente_id == Cliente.id
    ).filter(
        Cliente.usuario_id == current_user.id
    ).group_by(
        Cliente.id
    ).all()
    
    clientes_formatados = []
    for cliente, total in resultados:
        cliente.equipamentos_ativos = total 
        clientes_formatados.append(cliente)

    return clientes_formatados