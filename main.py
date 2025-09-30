from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv() #Carrega as variáveis de ambiente do arquivo .env
SECRET_KEY = os.getenv("SECRET_KEY")

# para rodar o codigo: python -m uvicorn main:app --reload
app = FastAPI()

bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# importando as rotas
from auth_routes import auth_router
from item_routes import item_router

app.include_router(auth_router)
app.include_router(item_router)

