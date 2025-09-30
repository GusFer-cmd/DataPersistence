from models import db
from sqlalchemy.orm import sessionmaker

def catch_session():
    try: #Coloca um try para indepententemente do que aconteça, fechar a sessão
        Session = sessionmaker(bind=db) #Cria uma sessão, vinculando o banco de dados
        session = Session() #Cria uma instância de sessão
        yield session #Garante o fechamento
    finally:
        session.close() #Fecha a sessão