from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Usuario(base):
    __tablename__ = 'Usuario'
    id_cliente = Column(BigInteger, primary_key=True)
    nome = Column(String(256))
    password = Column(String(256))
    dt_nasc = Column(String(30))
    email = Column(String(256))
    telefone = Column(String(256))
    cpf = Column(String(256))
    sobrenome = Column(String(256))
    user_type = Column(String(256))
    delete = Column(SmallInteger, default= 0)

