from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional

class EquipamentoBase(BaseModel):
    nome:str
    categoria: Optional[str] = None
    numero_patrimonio: str
    valor_diaria: Decimal

class EquipamentoCreate(EquipamentoBase):
    pass

class EquipamentoResponse(EquipamentoBase):
    id: int
    status_equipamento: str
    model_config = ConfigDict(from_attributes=True)
