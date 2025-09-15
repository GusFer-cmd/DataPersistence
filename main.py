from fastapi import FastAPI

# para rodar o codigo: python -m uvicorn main:app --reload
app = FastAPI()

# importando as rotas
from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

