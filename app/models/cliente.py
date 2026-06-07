from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.config.settings import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_razao_social = Column(String, nullable=False)
    cnpj = Column(String, unique=True, index=True, nullable=False)
    email_contato = Column(String)
    telefone_contato = Column(String)
    ativo = Column(Boolean, default=True)

    locacoes = relationship("Locacao", back_populates="cliente")