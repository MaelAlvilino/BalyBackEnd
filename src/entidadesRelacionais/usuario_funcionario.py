from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Usuario_Funcionario(base):
    __tablename__ = 'Usuario_Funcionario'
    idusuario_funcionario = Column(BigInteger, primary_key=True)
    nome = Column(String(256))
    password = Column(String(256))
    especialidade = Column(String(256))
    email = Column(String(256))
    user_type = Column(String(256))
    delete = Column(SmallInteger, default= 0)