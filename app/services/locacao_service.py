from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.equipamento import Equipamento, StatusEquipamento
from app.models.locacao import Locacao
from app.schemas.locacao import LocacaoCreate
from datetime import datetime
from app.models.manutencao import Manutencao
from app.schemas.locacao import CheckInRequest
from app.models.locacao import StatusLocacao

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

def fazer_checkin(db: Session, dados_checkin: CheckInRequest):
    locacao = db.query(Locacao).filter(
        Locacao.id == dados_checkin.locacao_id,
        Locacao.status_locacao == StatusLocacao.ATIVA.value
    ).first()

    if not locacao:
        raise HTTPException(status_code=404, detail="Locação ativa não encontrada")
    
    equipamento = db.query(Equipamento).filter(Equipamento.id == locacao.equipamento_id).first()

    locacao.data_devolucao_real = datetime.now()
    locacao.status_locacao = StatusLocacao.CONCLUIDA.value

    if dados_checkin.possui_avaria:
        equipamento.status_equipamento = StatusEquipamento.EM_MANUTENCAO.value

        nova_manutencao = Manutencao(
            equipamento_id = equipamento.id,
            locacao_id=locacao.id,
            descricao_avaria=dados_checkin.descricao_avaria or "Avaria não detalhada"
        )
        db.add(nova_manutencao)

    else:
        equipamento.status_equipamento = StatusEquipamento.DISPONIVEL.value

    db.commit()
    db.refresh(locacao)

    return {
        "mensagem": "Check-in realizado com sucesso",
        "status_equipamento": equipamento.status_equipamento
    }