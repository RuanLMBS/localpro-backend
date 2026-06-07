import enum
from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.settings import Base

class StatusLocacao(enum.Enum):
    ATIVA = "Ativa"
    CONCLUIDA = "Concluída"

class Locacao(Base):
    __tablename__ = "locacoes"

    id = Column(Integer, primary_key=True, index=True)
    equipamento_id = Column(Integer, ForeignKey("equipamentos.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    
    data_saida = Column(DateTime(timezone=True), server_default=func.now())
    data_prevista_devolucao = Column(Date, nullable=False)
    data_devolucao_real = Column(DateTime(timezone=True), nullable=True)
    
    status_locacao = Column(
        SQLEnum(StatusLocacao, native_enum=False, length=50), 
        default=StatusLocacao.ATIVA
    )

    equipamento = relationship("Equipamento", back_populates="locacoes")
    cliente = relationship("Cliente", back_populates="locacoes")
    manutencoes = relationship("Manutencao", back_populates="locacao")