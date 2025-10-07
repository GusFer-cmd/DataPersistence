from fastapi import APIRouter, Depends, HTTPException
from models import Item, User, ItemCompra
from dependencies import catch_session, verify_tokenJWT
from schemas import ItemSchema, UserSchema, ItemCompraSchema
from sqlalchemy.orm import Session

itemcompras_router = APIRouter(prefix="/itemcompra", tags=["itemcompra"], dependencies=[Depends(verify_tokenJWT)]) #Posso usar como middleware e passar a dependendia verify_tokenJWT

@itemcompras_router.get("/list/{user_id}")
async def list(user_id: int, user: User = Depends(verify_tokenJWT), session: Session = Depends(catch_session)):
    if not user.admin and user.id != user_id:
        raise HTTPException(status_code=403, detail="Apenas administradores podem listar os itens de compra de outros usuários")
    else:
        itemcompras = session.query(ItemCompra).filter(ItemCompra.user_id == user_id).all()

    return {
        "itemcompras": itemcompras
    }

@itemcompras_router.post("/create/{item_id}")
async def create(item_id: int, itemcompra_schema: ItemCompraSchema, session: Session = Depends(catch_session), user: User = Depends(verify_tokenJWT)):
    #Realiza as consultas 
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    new_itemcompra = ItemCompra(item_id=item_id, user_id=user.id, quantity=itemcompra_schema.quantity)
    session.add(new_itemcompra)
    session.commit()
    return {"mensagem" : f"ItemCompra adicionado com sucesso: {new_itemcompra.id}"}

@itemcompras_router.delete("/delete/{itemcompra_id}")
async def delete(itemcompra_id: int, session: Session = Depends(catch_session), user: User = Depends(verify_tokenJWT)):
    itemcompra = session.query(ItemCompra).filter(ItemCompra.id == itemcompra_id).first()
    if not itemcompra:
        raise HTTPException(status_code=404, detail="ItemCompra não encontrado")
    if not user.admin and itemcompra.user_id != user.id:
        raise HTTPException(status_code=403, detail="Apenas administradores podem deletar itens de compra de outros usuários")
    session.delete(itemcompra)
    session.commit()
    return {"mensagem": "ItemCompra deletado com sucesso"}