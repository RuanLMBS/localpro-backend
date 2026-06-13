from sqlalchemy.orm import Session
from app.models.equipamento import Equipamento
from app.models.locacao import Locacao
from app.models.manutencao import Manutencao

def obter_resumo_inventario(db: Session, user_id):
    equipamentos = db.query(Equipamento).filter(
        Equipamento.usuario_id == user_id
    ).all()
    
    lista_formatada = []
    
    for eq in equipamentos:
        item = {
            "id": eq.id,
            "nome": eq.nome,
            "numero_patrimonio": eq.numero_patrimonio,
            "categoria": eq.categoria, 
            "status_equipamento": eq.status_equipamento,
            "cliente": None,
            "data_prevista_devolucao": None,
        }

        if eq.status_equipamento == "Alugado": 
            locacao_ativa = db.query(Locacao).filter(
                Locacao.equipamento_id == eq.id,
                Locacao.data_devolucao_real == None
            ).first()

            if locacao_ativa:
                item["cliente"] = locacao_ativa.cliente.nome_razao_social
                item["data_prevista_devolucao"] = locacao_ativa.data_prevista_devolucao
                item["locacao_id"] = locacao_ativa.id

        elif eq.status_equipamento == "Em Manutenção":
            manutencao_ativa = db.query(Manutencao).filter(
                Manutencao.equipamento_id == eq.id,
                Manutencao.data_conclusao == None
            ).first()
            
            if manutencao_ativa:
                item["manutencao_id"] = manutencao_ativa.id

        lista_formatada.append(item)

    return {
        "total": len(equipamentos),
        "disponiveis": sum(1 for e in equipamentos if e.status_equipamento == "Disponível"),
        "alugados": sum(1 for e in equipamentos if e.status_equipamento == "Alugado"),
        "manutencao": sum(1 for e in equipamentos if e.status_equipamento == "Em Manutenção"),
        "equipamentos": lista_formatada
    }