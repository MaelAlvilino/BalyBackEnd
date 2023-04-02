from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Agenda(base):
    __tablename__ = 'Agendar'
    id_Agenda = Column(BigInteger, primary_key=True)
    data_hora = Column(String(30))
    idusuario_funcionario = Column(BigInteger)
    id_cliente = Column(BigInteger)
