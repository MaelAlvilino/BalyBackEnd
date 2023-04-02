from dataclasses import dataclass
@dataclass
class Usuario_Funcionario:
    email : str
    nome : str
    password : str
    especialidade : str
    user_type: str