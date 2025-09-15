from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["autenticate"])

@auth_router.get("/login")
async def login():
    """
    Essa é a rota de login do nosso sistema.
    """

    return {"mensagem" : "Você acessou a rota de login"}
