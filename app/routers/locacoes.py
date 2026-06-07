from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.locacao import LocacaoCreate, LocacaoResponse
from app.services.locacao_service import fazer_checkout
from app.schemas.locacao import LocacaoCreate, LocacaoResponse, CheckInRequest
from app.services.locacao_service import fazer_checkin, fazer_checkout

router = APIRouter(prefix="/api/locacoes", tags=["Locações"])

@router.post("/checkout", response_model=LocacaoResponse, status_code=status.HTTP_201_CREATED)
def checkout_equipamento(locacao: LocacaoCreate, db: Session = Depends(get_db)):
    nova_locacao = fazer_checkout(db=db, locacao_dados=locacao)
    return nova_locacao

@router.post("/checkin", status_code=status.HTTP_200_OK)
def checkin_equipamento(dados: CheckInRequest, db: Session = Depends(get_db)):
    resultado = fazer_checkin(db=db, dados_checkin=dados)
    return resultado