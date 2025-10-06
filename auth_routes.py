from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import catch_session, verify_tokenJWT
from main import bycrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["autenticate"])

# Função para criar um token JWT (simulado aqui)
def create_tokenJWT(user_id, duration_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expire_date = datetime.now(timezone.utc) + duration_token # Data de expiração do token
    info = {
        "sub": str(user_id),
        "exp": expire_date
    }
    jwt_decode = jwt.encode(info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_decode

def authenticate_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bycrypt_context.verify(password, user.password): #Senha digitada é igual a do banco?
        return False
    return user

@auth_router.get("/")
async def home():
    """
    Essa é a rota de register do nosso sistema.
    """

    return {"mensagem" : f"Você acessou a rota de register", "autenticado": False}

# def create_first_admin(session: Session = Depends(catch_session)):
#     any_admin = session.query(User).filter(User.admin == True).first()
#     if not any_admin:
#         crypto_password = bycrypt_context.hash("senha_super_segura")
#         admin = User(
#             name="Admin Inicial",
#             email="admin@empresa.com",
#             password=crypto_password,
#             active=True,
#             admin=True
#         )
#         session.add(admin)
#         session.commit()

@auth_router.post("/register")
async def register(user_schema: UserSchema, session: Session = Depends(catch_session), user: User = Depends(verify_tokenJWT)):
    #Apenas usuários administradores podem criar novos usuários administradores
    if user_schema.admin and not user.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem criar novos usuários administradores")
    #Realiza as consultas
    user = session.query(User).filter(User.email == user_schema.email).first()
    if (user):
        #User já existe
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    else:
        crypto_password = bycrypt_context.hash( user_schema.password)
        new_user = User(name=user_schema.name, email=user_schema.email, password=crypto_password, active=user_schema.active, admin=user_schema.admin)
        session.add(new_user)
        session.commit()

        return {"mensagem": f"Usuário cadastrado com sucesso: {new_user.email}"}
    

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(catch_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session) #Chama a função que autentica o usuário
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não cadastrado ou credencias inválidas")
    else:
        access_token = create_tokenJWT(user.id)
        refresh_token = create_tokenJWT(user.id, duration_token=timedelta(days=7)) #No caso, o refresh token é igual ao access token
        return {
            "access_token": access_token,
            "refresh_token": refresh_token, 
            "token_type": "Bearer"
        }

#Função para o Autorize form do FASTAPI
@auth_router.post("/login-form")
async def login_form(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(catch_session)):
    user = authenticate_user(form_data.username, form_data.password, session) #Chama a função que autentica o usuário
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não cadastrado ou credencias inválidas")
    else:
        access_token = create_tokenJWT(user.id)
        refresh_token = create_tokenJWT(user.id, duration_token=timedelta(days=7)) #No caso, o refresh token é igual ao access token
        return {
            "access_token": access_token,
            "refresh_token": refresh_token, 
            "token_type": "Bearer"
        }                
    
@auth_router.get("/refresh_token")
async def refresh_token(user: User = Depends(verify_tokenJWT)):
    access_token = create_tokenJWT(user.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }      
