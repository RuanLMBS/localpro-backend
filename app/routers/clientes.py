# app/routers/clientes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse

from app.services.cliente_service import create_client

from sqlalchemy import func
from app.models.locacao import Locacao

from app.config.security import get_actual_user

router = APIRouter(
    prefix="/api/clientes", 
    tags=["Clientes"],
    dependencies=[Depends(get_actual_user)]
    )

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(cliente_in: ClienteCreate, db: Session = Depends(get_db), current_user=Depends(get_actual_user)):
    try:
        return create_client(db, cliente_in, current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), current_user = Depends(get_actual_user)):
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