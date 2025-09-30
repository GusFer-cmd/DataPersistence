from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import catch_session
from main import bycrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["autenticate"])

@auth_router.get("/")
async def register():
    """
    Essa é a rota de register do nosso sistema.
    """

    return {"mensagem" : "Você acessou a rota de register", "autenticado": False}

@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session = Depends(catch_session)):
    #Realiza as consultas
    user = session.query(User).filter(User.email == user_schema.email).first()
    if (user):
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    else:
        crypto_password = bycrypt_context.hash( user_schema.password)
        new_user = User(name=user_schema.name, email=user_schema.email, password=crypto_password, active=user_schema.active, admin=user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso {user_schema.email}"}