from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Procedimento(base):
    __tablename__ = 'Procedimento'
    id_Procedimento = Column(BigInteger, primary_key=True)
    nome = Column(String(100))
    tipo = Column(String(100))
    Duração_mendia = Column(String(30))
    descrição = Column(String(1000))