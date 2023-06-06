from sqlalchemy import BigInteger, Column, SmallInteger, String
from src.database.base import base

class Formularios(base):
    __tablename__ = 'Formularios'
    id_Formulario = Column(BigInteger, primary_key=True, autoincrement=True)
    email_cliente = Column(String(254))
    nome = Column(String(100))
    nome_procedimento = Column(String(100))
    cpf = Column(BigInteger)
    alergia = Column(String(1000))
    comentario = Column(String(1000))
    data_hora = Column(String(30))
    status = Column(String(15))