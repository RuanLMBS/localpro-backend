from pydantic import BaseModel, ConfigDict
from typing import Optional

class ClienteBase(BaseModel):
    nome_razao_social:str
    cnpj: str
    email_contato: Optional[str] = None
    telefone_contato: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    nome_razao_social:str
    cnpj: str
    telefone_contato: Optional[str] = None
    email_contato: Optional[str] = None
    ativo: bool

    equipamentos_ativos: int = 0

    model_config = ConfigDict(from_attributes=True)