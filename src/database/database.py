import os
from sqlalchemy import create_engine
from src.entidadesRelacionais import *
from .base import base
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from sqlalchemy.orm import Session

class Database():
    __dialect: str
    __databaseName: str
    __uri: str
    __port: str
    __username: str
    __password: str

    echo: bool = False
    base: declarative_base
    engine: create_engine
    session: Session

    def __init__(self, create_all=False, pool_size=1, max_overflow = 2, pool_timeout=300, pool_recycle=300) -> None :
        self.__dialect = 'mysql'
        self.__uri = 'localhost'
        self.__port = '3306'
        self.__databaseName = 'baly sistema'
        self.__username = 'root'
        self.__password = '220201'

        self.pool_size=pool_size
        self.max_overflow = max_overflow  
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle
        
        self.base = base

        string_url = f'{self.__dialect}://{self.__username}:{self.__password}@{self.__uri}:{self.__port}/{self.__databaseName}'

        self.engine = create_engine(
            string_url, 
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
            pool_timeout=pool_timeout,
            pool_use_lifo=True,
            echo=self.echo
        )
        self.session = sessionmaker(bind=self.engine)
        self.session_scoped = scoped_session(sessionmaker(bind=self.engine))

        if(create_all): self.create_all()

    def create_all(self) -> None:
        self.base.metadata.create_all(self.engine)