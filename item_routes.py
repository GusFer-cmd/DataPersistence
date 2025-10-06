from fastapi import APIRouter, Depends, HTTPException
from models import Item, User
from dependencies import catch_session, verify_tokenJWT
from schemas import ItemSchema
from sqlalchemy.orm import Session

item_router = APIRouter(prefix="/item", tags=["item"], dependencies=[Depends(verify_tokenJWT)]) #Posso usar como middleware e passar a dependendia verify_tokenJWT

@item_router.get("/list")
async def list(user: User = Depends(verify_tokenJWT) ,session: Session = Depends(catch_session)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem listar os itens")
    else:
        items = session.query(Item).all()

    return {
        "items": items
    }

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

@item_router.put("/update/{item_id}")
async def update(item_id: int, item_schema: ItemSchema, session: Session = Depends(catch_session), user: User = Depends(verify_tokenJWT)):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    if not user.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem atualizar itens")
    
    #Atualiza os dados
    item.title = item_schema.title
    item.description = item_schema.description
    item.price = item_schema.price
    item.available = item_schema.available
    session.commit()
    return {
        "mensagem": f"Item atualizado com sucesso: {item.title}",
        "item": item
    }

@item_router.delete("/delete/{item_id}")
async def delete(item_id: int, session: Session = Depends(catch_session), user: User = Depends(verify_tokenJWT)):
    item = session.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    if not user.admin:
        raise HTTPException(status_code=403, detail="Apenas administradores podem deletar itens")
    session.delete(item)
    session.commit()
    return {
        "mensagem": f"Item deletado com sucesso: {item.title}",
        "item": item
    }