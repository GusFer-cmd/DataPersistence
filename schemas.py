#Força tipagem de dados
from pydantic import BaseModel
from typing import Optional

#Schema para usuário
class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False 

    class Config:
        from_attributes = True

#Schema para Login
class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True

#Schema para Item
class ItemSchema(BaseModel):
    title: str
    description: str
    price: float
    available: Optional[bool] = True

    class Config:
        from_attributes = True


#Schema para ItemCompra
class ItemCompraSchema(BaseModel):
    item_id: int
    user_id: int
    quantity: int

    class Config:
        from_attributes = True