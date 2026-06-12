from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID

class UsuarioBase(BaseModel):
    nome:str
    email:str 
    nome_locadora: str 

class UsuarioCreate(UsuarioBase):
    senha: str

class UsuarioResponse(UsuarioBase):
    id: int
    nome: str
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)