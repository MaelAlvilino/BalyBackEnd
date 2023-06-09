from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Agenda(base):
    __tablename__ = 'Agenda'
    id_Agenda = Column(BigInteger, primary_key=True)
    data_hora = Column(String(30))
    email_func = Column(String(254))
    cpf_cliente = Column(BigInteger)
    nome_proc = Column(String(100))
    comentario_form = Column(String(1000))
    status = Column(String(20))
