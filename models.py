from sqlalchemy import Column, String, Integer
from flask import Flask, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

database_file = "sqlite:///banco1.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SECRET_KEY = 'SECRET_KEY'
app.secret_key = SECRET_KEY

class Usuario(db.Model):
    idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(130))
    statusUs = db.Column(db.CHAR(40))

    disciplina = db.relationship('Disciplina', backref='usuario', lazy=True)

    def __init__(self):
        return

    def __init__(self, login, senha):
        self.login = login
        self.senha = generate_password_hash(senha)
        self.statusUs = 'ativo'


    def set_password(self, senha):
        self.senha = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha, senha)

    def get_login(self):
        return self.login

    def get_idUsuario(self):
        return self.idUsuario

    def desativarUsuario(self):
        self.statusUs = 'inativo'


class Disciplina(db.Model):
    idDisciplina = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeDisciplina = db.Column(db.String(40))
    statusDisc = db.Column(db.CHAR(40))
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    assunto = db.relationship('Assunto', backref='disciplina', lazy=True)

    def __init__(self, nomeDisciplina):
        self.nomeDisciplina = nomeDisciplina
        self.statusDisc = 'ativo'
        self.idUsuario = session.get('idUsuario')


    def get_nomeDisciplina(self):
        return self.nomeDisciplina

    def get_idDisciplina(self):
        return self.idDisciplina

    def get_idUsuario(self):
        return self.idUsuario

    def set_nomeDisciplina(self, nomeDisciplina):
        self.nomeDisciplina = nomeDisciplina

    def desativarDisciplina(self):
        self.statusDisc = 'inativo'



class Assunto(db.Model):
    idAssunto = db.Column(db.Integer,primary_key=True,autoincrement=True)
    nomeAssunto = db.Column(db.String(40))
    statusAss = db.Column(db.String(40))
    idDisciplina = db.Column(db.Integer, db.ForeignKey('disciplina.idDisciplina'), nullable=False)
    questao = db.relationship('Questao',backref='assunto',lazy=True)


    def __init__(self, nomeAssunto,idDisciplina):
        self.nomeAssunto = nomeAssunto
        self.statusAss = 'ativo'
        self.idDisciplina = idDisciplina



    def get_nomeAssunto(self):
        return self.nomeAssunto

    def get_idAssunto(self):
        return self.idAssunto

    def get_idDisciplina(self):
        return self.idDisciplina

    def set_idDisciplina(self,idDisciplina):
        self.idDisciplina = idDisciplina

    def set_nomeAssunto(self, nomeAssunto):
        self.nomeAssunto = nomeAssunto

    def desativarAssunto(self):
        self.statusAss = 'inativo'




class Avaliacao(db.Model):
    idAvaliacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numerodeQuestoes = db.Column(db.String(40))
    nomeAvaliacao = db.Column(db.String(40))
    semestre = db.Column(db.String(40))
    ano = db.Column(db.String(40))
    statusAv = db.Column(db.CHAR(40))
    idDisciplina = db.Column(db.Integer, db.ForeignKey('disciplina.idDisciplina'), nullable=False)
    avaliacoesquestao = db.relationship('AvaliacoesQuestao', backref='avaliacao', lazy=True)


    def get_nomeAvaliacao(self):
        return self.nomeAvaliacao

    def get_semestre(self):
        return self.semestre

    def get_ano(self):
        return self.ano

    def get_idDisciplina(self):
        return self.idDisciplina

    def get_numerodeQuestoes(self):
        return self.numerodeQuestoes

    def set_nomeAvaliacao(self,nomeAvaliacao):
        self.nomeAvaliacao=nomeAvaliacao

    def set_semestre(self,semestre):
        self.semestre=semestre

    def set_ano(self,ano):
        self.ano=ano

    def set_numerodeQuestoes(self,numerodeQuestoes):
        self.numerodeQuestoes=numerodeQuestoes

    def desativarAvaliacao(self):
        self.statusAv='inativo'


class Questao(db.Model):
    idQuestao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pergunta = db.Column(db.String(255))
    tipo = db.Column(db.CHAR(40))
    vezesUsada = db.Column(db.Integer)
    resposta = db.Column(db.String(255))
    statusQ = db.Column(db.CHAR(40))
    idAssunto = db.Column(db.Integer, db.ForeignKey('assunto.idAssunto'), nullable=False)
    alternativas = db.relationship('Alternativas', backref='questao', lazy=True)
    avaliacoesquestao = db.relationship('AvaliacoesQuestao',backref='questao',lazy=True)

    def get_pergunta(self):
        return self.pergunta

    def get_resposta(self):
        return self.resposta

    def get_vezesUsada(self):
        return self.vezesUsada

    def get_tipo(self):
        return self.tipo

    def get_idAssunto(self):
        return self.idAssunto

    def get_idQuestao(self):
        return self.idQuestao

    def set_resposta(self,resposta):
        self.resposta= resposta

    def set_pergunta(self, pergunta):
        self.pergunta = pergunta

    def plusvezesUsada(self):
        self.vezesUsada+=1

    def set_tipo(self,tipo):
        self.tipo = tipo

    def set_idAssunto(self, idAssunto):
        self.idAssunto = idAssunto

    def desativarQuestao(self):
        self.statusQ = 'inativo'




class Alternativas(db.Model):
    idAlternativas = db.Column(db.Integer, primary_key=True, autoincrement=True)
    statusAl = db.Column(db.CHAR(40))
    alternativa = db.Column(db.CHAR(255))
    idQuestao = db.Column(db.Integer, db.ForeignKey('questao.idQuestao'), nullable=False)
    idAssunto = db.Column(db.Integer, db.ForeignKey('assunto.idAssunto'), nullable=False)

    def get_idAlternativas(self):
        return self.idAlternativas

    def get_statusAl(self):
        return self.statusAl

    def get_alternativa(self):
        return self.alternativa

    def get_idQuestao(self):
        return self.idQuestao

    def get_idAssunto(self):
        return self.idAssunto

    def desativarAlternativa(self):
        self.statusAl='inativo'

    def set_alternativa(self,alternativa):
        self.alternativa=alternativa


class AvaliacoesQuestao(db.Model):
    idAvaliacoesQuestao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idAvaliacao = db.Column(db.Integer, db.ForeignKey('avaliacao.idAvaliacao'))
    idQuestao = db.Column(db.Integer, db.ForeignKey('questao.idQuestao'))

    def get_idQuestao(self):
        return self.idQuestao

    def get_idAvaliacao(self):
        return self.idAvaliacao

    def set_idQuestao(self,idQuestao):
        self.idQuestao = idQuestao

    def set_idAvaliacao(self,idAvaliacao):
        self.idAvaliacao=idAvaliacao