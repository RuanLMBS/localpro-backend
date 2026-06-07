from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.config.security import verificar_senha, criar_token_acesso, gerar_hash_senha

router = APIRouter(prefix="/api/auth", tags=["Autenticação"])

def registrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    
    senha_criptografada = gerar_hash_senha(usuario_in.senha)
    
    novo_usuario = Usuario(
        nome=usuario_in.nome,
        email=usuario_in.email,
        nome_locadora=usuario_in.nome_locadora,
        senha_hash=senha_criptografada
    )
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
        
    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    token = criar_token_acesso(dados={"sub": usuario.email, "id": usuario.id})
    
    return {"access_token": token, "token_type": "bearer"}