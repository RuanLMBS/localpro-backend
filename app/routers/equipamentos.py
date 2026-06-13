# app/routers/equipamentos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.equipamento import Equipamento
from app.schemas.equipamento import EquipamentoCreate, EquipamentoResponse, HistoricoEvent
from datetime import  datetime, date

from app.routers.auth import ler_usuario_atual

from app.services.equipamento_service import obter_resumo_inventario

router = APIRouter(prefix="/api/equipamentos", tags=["Equipamentos"])

@router.post("/", response_model=EquipamentoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_equipamento(
    equip_in: EquipamentoCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(ler_usuario_atual)
):
    
    novo_equipamento = Equipamento(
        **equip_in.model_dump(),
        usuario_id=current_user.id 
    )

    db.add(novo_equipamento)
    db.commit()
    db.refresh(novo_equipamento)

    return novo_equipamento

@router.get("/", response_model=List[EquipamentoResponse])
def listar_equipamentos(db: Session = Depends(get_db), current_user = Depends(ler_usuario_atual)):
    return db.query(Equipamento).filter(Equipamento.usuario_id == current_user.id).all()

@router.get("/{id}/historico", response_model=List[HistoricoEvent])
def pegar_historico_equipamento(id: int, db: Session = Depends(get_db), current_user = Depends(ler_usuario_atual)):
    
    equipamento = db.query(Equipamento).filter(
        Equipamento.id == id,
        Equipamento.usuario_id == current_user.id
    ).first()
    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado.")

    eventos_brutos = []

    for loc in equipamento.locacoes:
        eventos_brutos.append({
            "ev": "Check-out",
            "raw_date": loc.data_saida,
            "desc": f"Vinculado a {loc.cliente.nome_razao_social}",
            "color": "var(--violet)"
        })

        if loc.data_devolucao_real:
            eventos_brutos.append({
                "ev": "Check-in",
                "raw_date": loc.data_devolucao_real,
                "desc": "Devolvido ao estoque",
                "color": "var(--green)"
            })

    for man in equipamento.manutencoes:
        data_hora = datetime.combine(man.data_entrada, datetime.min.time()) if type(man.data_entrada) is date else man.data_entrada
        
        eventos_brutos.append({
            "ev": "Em manutenção",
            "raw_date": data_hora,
            "desc": f"Avaria: {man.descricao_avaria}",
            "color": "var(--amber)"
        })

    eventos_brutos.sort(key=lambda x: x["raw_date"], reverse=True)

    resultado_formatado = []
    for ev in eventos_brutos:
        resultado_formatado.append(HistoricoEvent(
            ev=ev["ev"],
            date=ev["raw_date"].strftime("%d/%m/%Y"),
            desc=ev["desc"],
            color=ev["color"]
        ))

    return resultado_formatado

@router.get("/resumo")
def pegar_resumo_inventario(db: Session = Depends(get_db), current_user = Depends(ler_usuario_atual)):
    resultado = obter_resumo_inventario(db=db, user_id=current_user.id)

    return resultado