from datetime import date
from dataclasses import dataclass
@dataclass
class Usuario:
    email : str
    telefone : int
    cpf  : int
    nome : str
    sobrenome : str
    password : str
    dt_nasc : date
    user_type: str