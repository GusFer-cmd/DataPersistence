from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv() #Carrega as variáveis de ambiente do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# para rodar o codigo: python -m uvicorn main:app --reload
app = FastAPI()

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

# importando as rotas
from auth_routes import auth_router
from item_routes import item_router

app.include_router(auth_router)
app.include_router(item_router)

