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

        #Atualizar Procedimento
@app.route("/atualizarProcedimento", methods = ['PUT'])
def atualizar_Procedimento ():
    if request.method== 'PUT':
        json = request.get_json()
        
        schema = {
            'id_Procedimento': {'type': 'string', 'required': True},
            'nome': {'type': 'string', 'required': True},
            'tipo': {'type': 'string', 'required': True},
            'Duração_mendia': {'type': 'string', 'required': True},
            'descricao': {'type': 'string', 'required': True},
            'imagem': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
                
        if( validate.validate(json) is not True):
            return validate.errors, 400
         
        db: Database = app.config['database']

        dbSession = db.session_scoped()

        procedimento = dbSession.query(Procedimento).filter_by(id_Procedimento=json.get('id_Procedimento')).first()
        
        if not procedimento:
            return "Erro ao alterar o Procedimento", 404

        procedimento.nome = json.get('nome')
        procedimento.tipo = json.get('tipo')
        procedimento.Duração_mendia = json.get('Duração_mendia')
        procedimento.descricao = json.get('descricao')
        procedimento.imagem = json.get('imagem')

        dbSession.commit()

        return 'Procedimento atualizado com sucesso.'

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
            'descricao': {'type': 'string', 'required': True},
            'imagem': {'type': 'string', 'required': True}
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
            descricao = json.get('descricao'),
            imagem = json.get('imagem')
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

@app.route("/consultar_Procedimento/<id_Procedimento>", methods = ['GET'])
def Consultar_Procedimento (id_Procedimento): 
        #json = request.get_json()

        #schema = {
        #    'nome': {'type': 'string', 'required': True}
        #}
        #validate = Validator(schema)
        
        # caso não tenha campo retorna error
        #if( validate.validate(json) is not True):
        #    return validate.errors, 400

        #nome_proc = json.get('nome')
        id_proc = id_Procedimento
        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        #proc = dbSession.query(Procedimento).filter(Procedimento.nome == nome_proc).first()
        proc = dbSession.query(Procedimento).filter(Procedimento.id_Procedimento == id_proc).first()
        #nome_p = proc.nome
        #desc_p = proc.descricao
        resultados = []
        retorno = {
            'procedimento': proc.nome,
            'descricao': proc.descricao,
            'imagem': proc.imagem
        }
        resultados.append(retorno)
        db.session_scoped.remove()
        if proc != None:
            return resultados,200
        else:
            return "Procedimento não encontrado",500

@app.route("/Procedimento", methods = ['GET'])
def Listar_Procedimento ():

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
        #desc_p = proc.descricao
        i = 0
        resultados = []
        while i < len(proc):
            retorno = {
                'procedimento': proc[i].nome,
                'descricao': proc[i].descricao,
                'imagem': proc[i].imagem,
                'id_Procedimento': proc[i].id_Procedimento
            }
            resultados.append(retorno)
            i += 1
        db.session_scoped.remove()
        if proc != None:
            return resultados,200
        else:
            return "Procedimento não encontrado",500



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
