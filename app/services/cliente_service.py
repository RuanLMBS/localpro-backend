from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.cliente import Cliente
from app.models.locacao import Locacao
from app.schemas.cliente import ClienteCreate
from fastapi import HTTPException
from app.repositories.cliente_repository import get_client_by_cnpj, add_client

def create_client(db: Session, client: ClienteCreate, user_id):
    try:
        client_exist = get_client_by_cnpj(db=db, cnpj = client.cnpj, user_id = user_id)
        
        if client_exist:
            raise HTTPException(status_code=400, detail="CNPJ já cadastrado.")
        
        new_client = add_client(db=db, new_client = client, user_id = user_id)
        return new_client
    except:
        raise Exception
    