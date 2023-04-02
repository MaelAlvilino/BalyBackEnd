from asyncio.windows_events import NULL
from tkinter import E
from flask import Flask, request, jsonify
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
            #Cadastrar Clientes
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
            'descrição': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        # json usuario que irá ser passado para o banco
        procedimento = Procedimento (
            nome = json.get('nome'),
            tipo = json.get('tipo'),
            Duração_mendia = json.get('duração_media'),
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
        

        #Consultar Procedimento

@app.route("/consultar_Procedimento", methods = ['GET'])
def Consultar_Procedimento (): 
        #json = request.get_json()

        #schema = {
        #    'nome': {'type': 'string', 'required': True}
        #}
        #validate = Validator(schema)
        
        # caso não tenha campo retorna error
        #if( validate.validate(json) is not True):
        #    return validate.errors, 400

        #nome_proc = json.get('nome')


        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        #proc = dbSession.query(Procedimento).filter(Procedimento.nome == nome_proc).first()
        proc = dbSession.query(Procedimento).all()
        #nome_p = proc.nome
        #desc_p = proc.descrição
        i = 0
        retorno = []
        while i < len(proc):
            retorno.append([proc[i].nome, proc[i].descrição])
            i += 1
        db.session_scoped.remove()
        if proc != None:
            return retorno,200
        else:
            return "Procedimento não encontrado",500

        #lista de nomes de procedimentos separados por ';'

@app.route("/Procedimento", methods = ['GET'])
def Listar_Procedimento ():

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       
        procs = dbSession.query(Procedimento.nome).all()
        i = 0
        #nome_procs = ''
        #letras = ''
        #letras_dois = ''
        array = []
        db.session_scoped.remove()
        while i < len(procs):
            array += procs[i]
            #if nome_procs != '':
            #    nome_procs += ';'
            #    
            #    letras = (str(procs[i])).replace("('", '')
            #    letras_dois = letras.replace("',)", '')
            #    nome_procs += letras_dois
            #else:
            #    letras = (str(procs[i])).replace("('", '')
            #    letras_dois += letras.replace("',)", '')                
            #    nome_procs += letras_dois
            i += 1
        if procs != None:
            return array,200
        else:
            return "Não há procedimentos encontrados",500
#passar pro emanuel que essa lista é limitada com procedimento1;procedimento2;
#separar cada procedimento por ;
#cada procedimento em um "quadradinho" (pode ser qualquer coisa, só sendo algo para listar e o cliente clicar e abrir as infos)
#as infos que vão ser apresentadas estão em consultar_Procedimento, usando a mesma delimitação (;)



    # Consulta o usuario ou o funcionario com user_type
@app.route("/usuarios/<email>", methods = ['GET'])
def usuarios(email):
        #json = request.get_json()

        #schema = {
        #    'email': {'type': 'string', 'required': True}
        #    }
        #validate = Validator(schema)
        #
        ## caso não tenha campo retorna error
        #if( validate.validate(json) is not True):
        #    return validate.errors, 400

    #o cara que veio no get
    #email x como parametro
    #user_type x como parametro

        #user_email = json.get('email')
        user_email = email
        db: Database = app.config['database']
        dbSession = db.session_scoped()



        usuario_func = dbSession.query(Usuario_Funcionario).filter(Usuario_Funcionario.email == user_email).first()
        usuario_cli = dbSession.query(Usuario).filter(Usuario.email == user_email).first()
        db.session_scoped.remove()
        if usuario_func != None:
            return usuario_func.user_type,200
        elif usuario_cli != None:
            return usuario_cli.user_type,200
        else:    
            return "Usuario não encontrado",404



    #Login do Cliente consultando no banco
@app.route("/login_Usuario", methods = ['POST'])
def Login_Usuario (): 
        json = request.get_json()

        schema = {
            'email': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': True},
            'user_type': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400

        user_email = json.get('email')
        user_password = json.get('password')
        users_type = json.get('user_type')



        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        usuario = dbSession.query(Usuario).filter(Usuario.email == user_email, Usuario.password == user_password, Usuario.user_type == users_type).first()
        db.session_scoped.remove()
        if usuario != None:
            return users_type,200
        else:
            return "Usuario não encontrado",500


    #Login do Funcionario consultando no banco
@app.route("/login_Funcionario", methods = ['POST'])
def Login_Funcionario (): 
        json = request.get_json()

        schema = {
            'email': {'type': 'string', 'required': True},
            'password': {'type': 'string', 'required': True},
            'user_type':{'type':'string','required':True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400

        userfun_email = json.get('email')
        userfun_password = json.get('password')
        userfun_user_type = json.get('user_type')


        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        usuario = dbSession.query(Usuario_Funcionario).filter(Usuario_Funcionario.email == userfun_email, Usuario_Funcionario.password == userfun_password, Usuario_Funcionario.user_type == userfun_user_type).first()
        db.session_scoped.remove()
        if usuario != None:
            return userfun_user_type,200
        else:
            return "Funcionario não encontrado",500




            #Cadastrando o Agendamento e validando o id do cliente e do funcionario
@app.route("/cadastrarAgendamento", methods = ['POST','GET'])
def cadastrar_Agendamento ():
    if request.method== 'POST':
        json = request.get_json()
        schema = {
            'data_hora': {'type': 'string', 'required': True},
            'email': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True}
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
        db.session_scoped.remove()

      #  """SELECT * FROM USUARIO
       # WHERE CPF = CPF_CLIENTE (VARIAVEL)"""


        Agendamento = Agenda (
            data_hora = json.get('data_hora'),
            idusuario_funcionario = funcionario.idusuario_funcionario,
            id_cliente = cliente.id_cliente
        )
        cadastrarBanco(Agendamento)

        return 'Agendamento criado com sucesso.',200


        
        
app.run(debug=True)
