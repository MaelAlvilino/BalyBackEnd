from asyncio.windows_events import NULL
from tkinter import E
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.entidadesRelacionais import usuario
from src.entidadesRelacionais.usuario_funcionario import Usuario_Funcionario
from src.entidadesRelacionais.usuario import Usuario
from src.entidadesRelacionais.Procedimento import Procedimento
from src.entidadesRelacionais.Agenda import Agenda
from src.entidadesRelacionais.Form import Formularios
from src.entidadesRelacionais.Consulta import Consulta
from cerberus import Validator
from src.database.database import Database
from datetime import datetime
from typing import Union
from sqlalchemy import select
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
            'nome_proc': {'type': 'string', 'required': True},
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

        procedimento.nome_proc = json.get('nome_proc')
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
            'nome_proc': {'type': 'string', 'required': True},
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
            nome_proc = json.get('nome_proc'),
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

        id_proc = id_Procedimento
        db: Database = app.config['database']
        dbSession = db.session_scoped()
       


        proc = dbSession.query(Procedimento).filter(Procedimento.id_Procedimento == id_proc).first()
        resultados = []
        retorno = {
            'procedimento': proc.nome_proc,
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

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        proc = dbSession.query(Procedimento).all()

        i = 0
        resultados = []
        while i < len(proc):
            retorno = {
                'procedimento': proc[i].nome_proc,
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

# Verificar Formulário

@app.route("/verificarFormulario/<email>", methods = ['GET'])
def verificar_Formulario (email):
    if request.method== 'GET':
        user_email = email
        
        db: Database = app.config['database']
        dbSession = db.session_scoped()
        
        usuario_cli = dbSession.query(Formularios).filter(Formularios.email_cliente == user_email).first()
        db.session_scoped.remove()
        if usuario_cli is None: 
            return 'Usuário não possui formulário',400
        else:
            return 'Usuário já possui formulário',200

#  Cliente Cadastrar formulário 
@app.route("/cadastrarFormulario/<email>", methods = ['POST'])
def cadastrar_Formulario (email):
    if request.method== 'POST':
        user_email = email
        json = request.get_json()
        
        # Validador de json cerberus 
        schema = {
            'nome': {'type': 'string', 'required': True},
            'nome_procedimento': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'alergia': {'type': 'string', 'required': True},
            'comentario': {'type': 'string', 'required': True},
            'data_hora': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
            
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400

        formularios = Formularios (
            nome = json.get('nome'),
            nome_procedimento = json.get('nome_procedimento'),
            cpf = json.get('cpf'),
            email_cliente = user_email,
            alergia = json.get('alergia'),
            comentario = json.get('comentario'),
            data_hora = json.get('data_hora'),
            status = 'Indefinido'
        )
        
        db: Database = app.config['database']

        dbSession = db.session_scoped()
        usuario_cli = dbSession.query(Formularios).filter(Formularios.email_cliente == user_email).first()
        print(usuario_cli)
        if usuario_cli is None:
            print("entrei no add e dei cadastraei")
            dbSession.add(formularios)
        else:
            print("entrei no merge e dei update")
            usuario_cli.nome = json.get('nome')
            usuario_cli.nome_procedimento = json.get('nome_procedimento')
            usuario_cli.cpf = json.get('cpf')
            usuario_cli.email_cliente = user_email
            usuario_cli.alergia = json.get('alergia')
            usuario_cli.comentario = json.get('comentario')
            usuario_cli.data_hora = json.get('data_hora')
            usuario_cli.status = 'Indefinido'
        dbSession.commit()

        db.session_scoped.remove()

        return "deu sucesso", 200


            #Cadastrando o Agendamento e validando o id do cliente e do funcionario
@app.route("/cadastrarAgendamento", methods = ['POST'])
def cadastrar_Agendamento ():
    if request.method== 'POST':
        json = request.get_json()
        schema = {
            'data_hora': {'type': 'string', 'required': True},
            'email': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'nome_proc': {'type': 'string', 'required': True},
            'comentario_form': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        db: Database = app.config['database']
        dbSession = db.session_scoped()

        db.session_scoped.remove()



        Agendamento = Agenda (
            data_hora = json.get('data_hora'),
            email_func = json.get('email'),
            cpf_cliente = json.get('cpf'),
            nome_proc = json.get('nome_proc'),
            comentario_form = json.get('comentario_form'),
            status = 'Aguardando'
        )
        cadastrarBanco(Agendamento)

        form = dbSession.query(Formularios).filter(Formularios.data_hora == json.get('data_hora'), Formularios.cpf == json.get('cpf'), Formularios.nome_procedimento == json.get('nome_proc')).first()
        cliente = dbSession.query(Usuario).filter(Usuario.cpf == json.get('cpf')).first()
        email_cli = cliente.email

        USER_EMAIL = os.getenv("USER_EMAIL")
        USER_PASSWORD = os.getenv("USER_PASSWORD")

        print(USER_EMAIL, USER_PASSWORD)
        smtp_host = 'smtp.office365.com'
        smtp_port = 587
        smtp_username = "andrey_super_teste_hehe@hotmail.com" 
        smtp_password = "SenhaDificil123"

        subject = 'Consulta marcada com sucesso! :)'
        body = f'Parabéns!\nEstamos notificando que a consulta do procedimento {form.nome_procedimento} solicitada por você foi aceita! Te esperamos as {form.data_hora}!'
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email_cli
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # envio
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        # atualizar status
        form.status = 'Aprovado'
        dbSession.commit()
        return 'Agendamento criado com sucesso.',200

# Recusar Formulário
@app.route("/recusarFormulario", methods = ['POST'])
def recusar_Formulario ():
    if request.method== 'POST':
        json = request.get_json()
        schema = {
            'data_hora': {'type': 'string', 'required': True},
            'email': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'nome_proc': {'type': 'string', 'required': True},
            'comentario_form': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        db: Database = app.config['database']
        dbSession = db.session_scoped()
        db.session_scoped.remove()

        form = dbSession.query(Formularios).filter(Formularios.data_hora == json.get('data_hora'), Formularios.cpf == json.get('cpf'), Formularios.nome_procedimento == json.get('nome_proc')).first()
        cliente = dbSession.query(Usuario).filter(Usuario.cpf == json.get('cpf')).first()
        email_cli = cliente.email

        USER_EMAIL = os.getenv("USER_EMAIL")
        USER_PASSWORD = os.getenv("USER_PASSWORD")

        print(USER_EMAIL, USER_PASSWORD)
        smtp_host = 'smtp.office365.com'
        smtp_port = 587
        smtp_username = "andrey_super_teste_hehe@hotmail.com" 
        smtp_password = "SenhaDificil123"

        subject = 'Consulta recusada! :('
        body = f'Sentimos muito,\nMas estamos notificando que a consulta do procedimento {form.nome_procedimento} solicitada por você foi recusada!'
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email_cli
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # envio
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        # atualizar status
        form.status = 'Recusado'
        dbSession.commit()
        return 'Formulário recusado com sucesso.',200

# Listar Formulários  onde o Funcionario vai olhar 
@app.route("/listar_Formularios", methods = ['GET'])
def Listar_Formularios ():

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        form = dbSession.query(Formularios).filter(Formularios.status == 'Indefinido').all()
        agendamentos = dbSession.query(Agenda).all()
        
        # Verificar e excluir os objetos correspondentes
        lista_form = []
        for formulario in form:
            encontrado = False
            for agendar in agendamentos:
                if (
                    formulario.nome_procedimento == agendar.nome_proc and
                    formulario.data_hora == agendar.data_hora and
                    formulario.comentario_form == agendar.comentario_form
                ):
                    encontrado = True
                    break
            if not encontrado:
                lista_form.append(formulario)


        i = 0
        resultados = []
        while i < len(lista_form):
            retorno = {
                'id_Formulario': lista_form[i].id_Formulario,
                'email_cliente': lista_form[i].email_cliente,
                'nome': lista_form[i].nome,
                'nome_procedimento': lista_form[i].nome_procedimento,
                'cpf': lista_form[i].cpf,
                'alergia': lista_form[i].alergia,
                'comentario': lista_form[i].comentario,
                'data_hora': lista_form[i].data_hora
            }
            resultados.append(retorno)
            i += 1
        db.session_scoped.remove()
        if lista_form != None:
            return resultados,200
        else:
            return "Formularios não encontrado",500

# Listar Agendamentos para Consulta EM TESTE
@app.route("/listar_Agendamentos", methods = ['GET'])
def Listar_Agendamentos ():

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        agendas = dbSession.query(Agenda).filter(Agenda.status == 'Aguardando').all()
        consultas = dbSession.query(Consulta).all()
        
        # Verificar e excluir os objetos correspondentes
        lista_agenda = []
        for agenda in agendas:
            encontrado = False
            for consulta in consultas:
                if (
                    agenda.nome_proc == consulta.nome_proc and
                    agenda.data_hora == consulta.data_hora and
                    agenda.comentario_form == consulta.comentario_form
                ):
                    encontrado = True
                    break
            if not encontrado:
                lista_agenda.append(agenda)

        i = 0
        resultados = []
        while i < len(lista_agenda):
            retorno = {
                'id_Agenda': lista_agenda[i].id_Agenda,
                'data_hora': lista_agenda[i].data_hora,
                'email_func': lista_agenda[i].email_func,
                'cpf_cliente': lista_agenda[i].cpf_cliente,
                'nome_proc': lista_agenda[i].nome_proc,
                'comentario_form': lista_agenda[i].comentario_form,
                'status': lista_agenda[i].status
            }
            resultados.append(retorno)
            i += 1
        db.session_scoped.remove()
        if lista_agenda != None:
            return resultados,200
        else:
            return "Agendas não encontrado",500


# Cadastrar consulta EM TESTE
@app.route("/cadastrarConsulta", methods = ['POST'])
def cadastrar_Consulta ():
    if request.method== 'POST':
        json = request.get_json()
        schema = {
            'data_hora': {'type': 'string', 'required': True},
            'email': {'type': 'string', 'required': True},
            'cpf': {'type': 'string', 'required': True},
            'nome_proc': {'type': 'string', 'required': True},
            'comentario_form': {'type': 'string', 'required': True}
        }
        validate = Validator(schema)
        
        # caso não tenha campo retorna error
        if( validate.validate(json) is not True):
            return validate.errors, 400
        
        db: Database = app.config['database']
        dbSession = db.session_scoped()

        db.session_scoped.remove()



        Consultar = Consulta (
            data_hora = json.get('data_hora'),
            email_func = json.get('email'),
            cpf_cliente = json.get('cpf'),
            nome_proc = json.get('nome_proc'),
            comentario_form = json.get('comentario_form')
        )
        cadastrarBanco(Consultar)


        agenda = dbSession.query(Agenda).filter(Agenda.data_hora == json.get('data_hora'), Agenda.cpf_cliente == json.get('cpf'), Agenda.nome_proc == json.get('nome_proc')).first()
        # atualizar status da agenda
        agenda.status = 'Aprovado'
        dbSession.commit()

        return 'Consulta criado com sucesso.',200

# Listar Agendamentos para Consulta EM TESTE
@app.route("/listar_Consultas", methods = ['GET'])
def Listar_Consultas ():

        db: Database = app.config['database']
        dbSession = db.session_scoped()
       

        consultas = dbSession.query(Consulta).all()

        i = 0
        resultados = []
        while i < len(consultas):
            retorno = {
                'id_Consulta': consultas[i].id_Consulta,
                'data_hora': consultas[i].data_hora,
                'email_func': consultas[i].email_func,
                'cpf_cliente': consultas[i].cpf_cliente,
                'nome_proc': consultas[i].nome_proc,
                'comentario_form': consultas[i].comentario_form
            }
            resultados.append(retorno)
            i += 1
        db.session_scoped.remove()
        if consultas != None:
            return resultados,200
        else:
            return "Consultas não encontrado",500

app.run(debug=True)
