from fastapi import APIRouter

item_router = APIRouter(prefix="/item", tags=["item"])

@item_router.get("/list")
async def listar():
    """
    Essa é a rota de listagem do nosso sistema.
    """

    return {"mensagem" : "Você acessou a rota de listagem"}