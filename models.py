from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base

# cria conexão com o banco de dados
db = create_engine("sqlite:///database/banco.db")

# cria a base do banco de dados
Base = declarative_base() 

# criar as classes/tabelas do banco
#User
class User(Base):
    __tablename__ = "users" #por padrão o SQLAlchemy cria o nome da tabela no plural e tudo minúsculo

    # comandos SQL
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    # função para inicializar a criação de um usuário
    def _init_(self, name, email, password, active, admin):
        self.name = name
        self.email = email
        self.password = password 
        self.active = active  
        self.admin = admin

# Item
class Item(Base):
    __tablename__ = "items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=False)
    price = Column("price", Integer, nullable=False)
    available = Column("available", Boolean, default=True)

    def _init_(self, title, description, price, available):
        self.title = title
        self.description = description
        self.price = price 
        self.available = available

#Item Compra
class ItemCompra(Base):
    __tablename__ = "item_compras"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    item_id = Column("item_id", ForeignKey("items.id"), nullable=False)
    user_id = Column("user_id", ForeignKey("users.id"), nullable=False)
    quantity = Column("quantity", Integer, nullable=False)

    def _init_(self, item_id, user_id, quantity):
        self.item_id = item_id
        self.user_id = user_id 
        self.quantity = quantity

# executa a criação dos metadados do seu banco (cria o banco de dados)