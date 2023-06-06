from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Consulta(base):
    __tablename__ = 'Consulta'
    id_Consulta = Column(BigInteger, primary_key=True)
    data_hora = Column(String(30))
    email_func = Column(String(254))
    cpf_cliente = Column(BigInteger)
    nome_proc = Column(String(100))
    comentario_form = Column(String(1000))
