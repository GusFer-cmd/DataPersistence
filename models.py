from sqlalchemy import create_engine, Column, Integer, String, Boolean

# cria conexão com o banco de dados
db = create_engine("sqlite:///database/banco.db")

# cria a base do banco de dados
Base = declarative_base()

# criar as classes/tabelas do banco
class User(Base):
    __tablename__ = "users" #por padrão o SQLAlchemy cria o nome da tabela no plural e tudo minúsculo

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)


# executa a criação dos metadados do seu banco (cria o banco de dados)