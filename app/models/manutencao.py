import enum
from sqlalchemy import Column, Integer, ForeignKey, Date, Text, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class StatusManutencao(enum.Enum):
    EM_REPARO = "Em Reparo"
    CONCLUIDO = "Concluído"

class Manutencao(Base):
    __tablename__ = "manutencoes"

    id = Column(Integer, primary_key=True, index=True)
    equipamento_id = Column(Integer, ForeignKey("equipamentos.id", ondelete="CASCADE"), nullable=False)
    locacao_id = Column(Integer, ForeignKey("locacoes.id", ondelete="SET NULL"), nullable=True)
    descricao_avaria = Column(Text, nullable=False)
    data_entrada = Column(Date, server_default=func.current_date())
    data_conclusao = Column(Date, nullable=True)
    
    status_manutencao = Column(
        SQLEnum(StatusManutencao, native_enum=False, length=50), 
        default=StatusManutencao.EM_REPARO
    )

    equipamento = relationship("Equipamento", back_populates="manutencoes")
    locacao = relationship("Locacao", back_populates="manutencoes")