from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.get("/list")
async def listar():
    """
    Essa é a rota de listagem do nosso sistema.
    """

    return {"mensagem" : "Você acessou a rota de listagem"}