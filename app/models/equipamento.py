import enum
from sqlalchemy import Column, Integer, String, Numeric, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class StatusEquipamento(str, enum.Enum):
    DISPONIVEL = "Disponível"
    ALUGADO = "Alugado"
    EM_MANUTENCAO = "Em Manutenção"

class Equipamento(Base):
    __tablename__ = "equipamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String)
    numero_patrimonio = Column(String, index=True, nullable=False)
    valor_diaria = Column(Numeric(10, 2), nullable=False)
    
    status_equipamento = Column(
        SQLEnum(StatusEquipamento, native_enum=False, length=50), 
        default=StatusEquipamento.DISPONIVEL
    )

    locacoes = relationship("Locacao", back_populates="equipamento")
    manutencoes = relationship("Manutencao", back_populates="equipamento")

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criador = relationship("Usuario", back_populates="equipamentos")