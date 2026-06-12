from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional
from app.schemas.equipamento import EquipamentoResponse


class ManutencaoCreate(BaseModel):
    equipamento_id: int
    locacao_id: Optional[int] = None
    descricao_avaria: str

class ManutencaoResponse(ManutencaoCreate):
    id: int
    data_entrada: date
    data_conclusao: Optional[date] = None
    status_manutencao: str
    equipamento: Optional['EquipamentoResponse'] = None
    model_config = ConfigDict(from_attributes=True)