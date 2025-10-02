from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import User
from jose import jwt, JWTError

def catch_session():
    try: #Coloca um try para indepententemente do que aconteça, fechar a sessão
        Session = sessionmaker(bind=db) #Cria uma sessão, vinculando o banco de dados
        session = Session() #Cria uma instância de sessão
        yield session #Garante o fechamento
    finally:
        session.close() #Fecha a sessão

def verify_tokenJWT(token: str = Depends(oauth2_schema), session: Session = Depends(catch_session)):
    try:
        info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return user

