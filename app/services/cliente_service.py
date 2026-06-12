from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cliente import Cliente
from app.models.locacao import Locacao

def listar_todos_clientes(db: Session):
    resultados = db.query(
        Cliente,
        func.count(Locacao.id).filter(Locacao.data_devolucao_real == None).label("total_ativos")
    ).outerjoin(
        Locacao, Locacao.cliente_id == Cliente.id
    ).group_by(
        Cliente.id
    ).all()

    clientes_formatados = []
    for cliente, total_ativos in resultados:
        cliente.equipamentos_ativos = total_ativos 
        clientes_formatados.append(cliente)

    return clientes_formatados