from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from typing import Optional

class LocacaoCreate(BaseModel):
    equipamento_id: int
    cliente_id: int
    data_prevista_devolucao: date

class LocacaoResponse(BaseModel):
    id: int
    equipamento_id: int
    cliente_id: int
    data_saida: datetime
    data_prevista_devolucao: date
    data_devolucao_real: Optional[datetime] = None
    status_locacao: str
    model_config = ConfigDict(from_attributes=True)

class CheckInRequest(BaseModel):
    locacao_id: int
    possui_avaria: bool
    descricao_avaria: Optional[str] = None