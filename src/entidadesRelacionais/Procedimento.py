from datetime import datetime
from sqlalchemy import BigInteger, Column, SmallInteger, String, DateTime
from src.database.base import base

class Procedimento(base):
    __tablename__ = 'Procedimento'
    id_Procedimento = Column(BigInteger, primary_key=True)
    nome_proc = Column(String(100))
    tipo = Column(String(100))
    Duração_mendia = Column(String(30))
    descricao = Column(String(1000))
    imagem = Column(String(1000))
    #Adicionar o Nome do Procedimento
    