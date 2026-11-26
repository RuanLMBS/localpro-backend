from sqlalchemy.orm import Session
from app.models.cliente import Cliente


def get_client_by_cnpj (db: Session, cnpj, user_id) -> Cliente | None:
    return db.query(Cliente).filter(
        Cliente.cnpj == cnpj,
        Cliente.usuario_id == user_id
    ).first()

def add_client(db: Session, new_client, user_id) -> Cliente:
    new_client = Cliente(**new_client.model_dump(), usuario_id=user_id)

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client