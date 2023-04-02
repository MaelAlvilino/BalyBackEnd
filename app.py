from asyncio.windows_events import NULL
from tkinter import E
from flask import Flask, request
from flask_cors import CORS
from src.entidadesRelacionais import usuario
from src.entidadesRelacionais.usuario_funcionario import Usuario_Funcionario
from src.entidadesRelacionais.usuario import Usuario
from src.entidadesRelacionais.Procedimento import Procedimento
from src.entidadesRelacionais.Agenda import Agenda
from cerberus import Validator
from src.database.database import Database
from datetime import datetime
from typing import Union
from sqlalchemy import select

app = Flask(__name__)

app.config['database'] = Database(create_all=True)
CORS(app)
            #Cadastrar Cliente
@app.route("/cadastro", methods = ['POST','GET'])
def cadastrar ():
    if request.method== 'POST':
        json = request.get_json()
        
        # Validador de json cerberus 
        schema = {
            'email': {'type': 'string', 'required': True},
            'telefone': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'nome': {'type': 'string', 'required': True},
            'sobrenome': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': True},
            'dt_nasc': {'type': 'string', 'required': True},
            'user_type': {'type': 'string', 'required': True} 
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        # json usuario que irá ser passado para o banco
        usuario = Usuario(
            email = json.get('email'),
            telefone = json.get('telefone'),
            cpf = json.get('cpf'),
            nome = json.get('nome'),
            sobrenome = json.get('sobrenome'),
            password = json.get('password'),
            dt_nasc = json.get('dt_nasc'), #datetime.strptime(json.get('dt_nasc'),'%d%m%y')
            user_type = json.get('user_type')
        )
        cadastrarBanco(usuario)

        return 'usuario criado com sucesso.'

        #Cadastrar Funcionario
@app.route("/cadastroFuncionario", methods = ['POST'])
def cadastrar_Funcionario ():
    json = request.get_json()

    # Validador de json cerberus 
    schema = {
        'email': {'type': 'string', 'required': True},
        'nome': {'type': 'string', 'required': True},
        'password': {'type': 'string', 'required': True},
        'especialidade': {'type': 'string', 'required': True},
        'user_type': {'type': 'string', 'required': True}
    }
    validate = Validator(schema)
    
    # caso não tenha campo retorna error
    if( validate.validate(json) is not True):
        return validate.errors, 400
    
    # json funcionario que irá ser passado para o banco
    usuario_funcionario = Usuario_Funcionario(
        email = json.get('email'),
        nome = json.get('nome'),
        password = json.get('password'),
        especialidade = json.get('especialidade'),
        user_type = json.get('user_type')
    )
    cadastrarBanco(usuario_funcionario)

    return 'Funcionário criado com sucesso.'

        #Cadastrar Procedimento
@app.route("/cadastroProcedimento", methods = ['POST','GET'])
def cadastrar_Procedimento ():
    if request.method== 'POST':
        json = request.get_json()
        
        # Validador de json cerberus 
        schema = {
            'nome': {'type': 'string', 'required': True},
            'tipo': {'type': 'string', 'required': True},
            'duração_media': {'type': 'string', 'required': True},
            'descrição': {'type': 'string', 'required': True},
            'user_type': {'type': 'string', 'required': True} 
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        # json usuario que irá ser passado para o banco
        procedimento = Procedimento (
            email = json.get('email'),
            tipo = json.get('tipo'),
            duração_media = json.get('duração_media'),
            descrição = json.get('descrição')
        )
        cadastrarBanco(procedimento)

        return 'Procedimento criado com sucesso.'

def cadastrarBanco(usuario: Union[Usuario,Usuario_Funcionario,Procedimento]):
    # acrescentar o banco
    db: Database = app.config['database']
    dbSession = db.session_scoped()
    dbSession.add(usuario)
    dbSession.commit()
    db.session_scoped.remove()
    
    # consultar o usuario no banco

        
@app.route("/login_Usuario", methods = ['POST'])
def Login_Usuario ():
        json = request.get_json()
        user_email = json.get('email')
        user_password = json.get('password')

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        usuario = dbSession.query(Usuario).filter(Usuario.email == user_email , Usuario.password == user_password).first()
        db.session_scoped.remove()
        if usuario != None:
            return "Usuario logado"
        else:
            return "Usuario não encontrado"

    #consultar o funcionario no banco

@app.route("/login_Funcionario", methods = ['POST'])
def Login_Funcionario ():
        json = request.get_json()
        user_email = json.get('email')
        user_password = json.get('password')

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        usuario_funcionario = dbSession.query(Usuario_Funcionario).filter(Usuario_Funcionario.email == user_email , Usuario_Funcionario.password == user_password).first()
        db.session_scoped.remove()
        if usuario_funcionario != None:
            return "Funcionario logado"
        else:
            return "Funcionario não encontrado"

#Fazer uma consulta pro Procedimento depois!!


            
@app.route("/cadastrarAgendamento", methods = ['POST','GET'])
def cadastrar_Agendamento ():
    if request.method== 'POST':
        json = request.get_json()
        schema = {
            'data_hora': {'type': 'string', 'required': True},
            'email': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'user_type': {'type': 'string', 'required': True} 
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        db: Database = app.config['database']
        dbSession = db.session_scoped()

        # json usuario que irá ser passado para o banco
        cpf_cliente = json.get('cpf')
        cliente = dbSession.query(Usuario).filter(Usuario.cpf == cpf_cliente).first()

        email_funcionario = json.get('email')
        funcionario = dbSession.query(Usuario_Funcionario).filter(Usuario_Funcionario.email == email_funcionario).first()
      #  """SELECT * FROM USUARIO
       # WHERE CPF = CPF_CLIENTE (VARIAVEL)"""


        Agendamento = Agenda (
            data_hora = json.get('data_hora'),
            idusuario_funcionario = funcionario.idusuario_funcionario,
            id_cliente = cliente.id_cliente
        )
        cadastrarBanco(Agendamento)

        return 'Agendamento criado com sucesso.'
        
app.run(debug=True)
