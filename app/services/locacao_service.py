from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.equipamento import Equipamento, StatusEquipamento
from app.models.locacao import Locacao
from app.schemas.locacao import LocacaoCreate

def fazer_checkout(db: Session, locacao_dados: LocacaoCreate):
    equipamento = db.query(Equipamento).filter(Equipamento.id == locacao_dados.equipamento_id).first()

    if not equipamento:
        raise HTTPException(status_code=404, detail="Equipamento não encontrado")
    
    if equipamento.status_equipamento != StatusEquipamento.DISPONIVEL.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Checkout negado: O equipamento está {equipamento.status_equipamento} ."
        )
    
    nova_locacao = Locacao(
        equipamento_id =locacao_dados.equipamento_id,
        cliente_id = locacao_dados.cliente_id,
        data_prevista_devolucao=locacao_dados.data_prevista_devolucao
    )

    equipamento.status_equipamento = StatusEquipamento.ALUGADO.value

    db.add(nova_locacao)
    db.commit()
    db.refresh(nova_locacao)

    return nova_locacao