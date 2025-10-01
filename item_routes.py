from fastapi import APIRouter, Depends, HTTPException
from models import Item
from dependencies import catch_session
from schemas import ItemSchema
from sqlalchemy.orm import Session

item_router = APIRouter(prefix="/item", tags=["item"])

@item_router.get("/list")
async def listar():
    """
    Essa é a rota de listagem do nosso sistema.
    """

    return {"mensagem" : "Você acessou a rota de listagem"}

@item_router.post("/create")
async def create(item_schema: ItemSchema, session: Session = Depends(catch_session)):
    #Realiza as consultas 
    item = session.query(Item).filter(Item.title == item_schema.title).first()
    if (item):
        #Item já existe
        raise HTTPException(status_code=400, detail="Item já cadastrado")
    else:
        new_item = Item(title=item_schema.title, description=item_schema.description, price=item_schema.price, available=item_schema.available)
        session.add(new_item)
        session.commit()
    return {"mensagem" : f"Item adicionado com sucesso: {new_item.title}"}