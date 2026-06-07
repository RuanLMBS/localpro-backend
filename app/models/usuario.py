from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.settings import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nome_locadora = Column(String, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())