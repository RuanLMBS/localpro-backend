from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome_razao_social = Column(String, nullable=False)
    cnpj = Column(String, index=True, nullable=False)
    email_contato = Column(String)
    telefone_contato = Column(String)
    ativo = Column(Boolean, default=True)

    locacoes = relationship("Locacao", back_populates="cliente")
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    criador = relationship("Usuario", back_populates="clientes")