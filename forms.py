from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FormField, SelectField, FieldList, DateField, \
    DateTimeField, BooleanField

from wtforms.validators import DataRequired

from models import Disciplina


class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    password = PasswordField('Senha', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    remember_me = BooleanField('Lembrar meu usuário e senha')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    password = StringField('Senha', validators=[DataRequired("O preenchimento desse campo é obrigatório")])
    submit = SubmitField('Cadastrar')

class CadastroDisciplinaForm(FlaskForm):
    nomeDisciplina = StringField('Nome disciplina', validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Cadastrar')

class ListarDisciplinasForm(FlaskForm):
    disciplinas = SelectField('Nome da disciplina',coerce=int)
    submitExcluir = SubmitField('Excluir Disciplina')
    submitEditar = SubmitField('Editar Disciplina')


class AssuntoForm(FlaskForm):
    nomeAssunto = StringField('Nome assunto', validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Cadastrar')

class EditarDisciplinaForm(FlaskForm):
    nomeDisciplina = StringField('Nome disciplina',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    novaDisciplina = StringField('Novo nome da disciplina',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Editar')


class CadastroAssuntoForm(FlaskForm):

    disciplinas = SelectField('Nome da Disciplina',coerce=int)
    nomeAssunto = StringField('Nome assunto', validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Cadastrar')

class ListarAssuntoForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina',coerce=int)
    assuntos = SelectField('Assuntos',coerce=int)
    submit1 = SubmitField('Listar')
    submit2 = SubmitField('Excluir')
    submit3 = SubmitField('Editar')

class EditarAssuntoForm(FlaskForm):
    nomeAssunto = StringField('Nome do Assunto atual',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    novoAssunto = StringField('Novo nome do Assunto',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Editar')

class CadastroQuestaoForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina',coerce=int)
    assuntos = SelectField('Nome do Assunto',coerce=int)
    submitListarAssuntos = SubmitField('Listar Assuntos')
    pergunta = StringField('Pergunta')
    resposta = StringField('Resposta')
    tipo = SelectField('Tipo',choices=[('Discursiva','Discursiva'),('Multipla Escolha','Multipla Escolha')])
    submitCadastro = SubmitField('Cadastrar')

class ListarQuestaoForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina', coerce=int)
    assuntos = SelectField('Nome do Assunto', coerce=int)
    questoes = SelectField('Pergunta da Questao',coerce=int)
    submitListarA = SubmitField('Listar Assuntos')
    submitListarQ = SubmitField('Listar Questoes')
    submitEditar = SubmitField('Editar Questao')
    submitExcluir = SubmitField('Excluir Questao')

class EditarQuestaoForm(FlaskForm):
    pergunta = StringField('Pergunta da questao atual')
    tipo = StringField('Tipo',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    novo_tipo = SelectField('Novo Tipo',choices=[('Discursiva','Discursiva'),('Multipla Escolha','Multipla Escolha')])
    nova_pergunta = StringField('Nova pergunta',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    nova_resposta = StringField('Nova resposta',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Editar')

class CadastroAlternativaForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina', coerce=int)
    assuntos = SelectField('Nome do Assunto', coerce=int)
    questoes = SelectField('Pergunta da Questao', coerce=int)
    submitListarAssunto = SubmitField('Listar Assuntos')
    submitListarQ = SubmitField('Listar Questoes')
    alternativa = StringField('Alternativa')
    submitCadastro = SubmitField('Cadastrar')

class ListarAlternativaForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina', coerce=int)
    assuntos = SelectField('Nome do Assunto', coerce=int)
    submitListarAss = SubmitField('Listar Assuntos')

    questoes = SelectField('Pergunta da Questao', coerce=int)
    submitListarQ = SubmitField('Listar Questoes')

    alternativas = SelectField('Alternativas',coerce=int)
    submitListarAl = SubmitField('Listar Alternativas')

    submitEditar = SubmitField('Editar Alternativa')
    submitExcluir = SubmitField('Excluir Alternativa')

class EditarAlternativaForm(FlaskForm):
    alternativa = StringField('Alternativa atual',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    nova_alternativa = StringField('Nova alternativa',validators=[DataRequired("O preenchimento desse campo é obrigatorio")])
    submit = SubmitField('Editar')

class CadastroAvaliacaoForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina',coerce=int)
    # assuntos = SelectField('Nome do Assunto',coerce=int)
    # submitListarAss = SubmitField('Listar Assuntos')
    nomeAvaliacao = StringField('Nome da Avaliacao')
    semestre = SelectField('Semestre da Avaliacao',choices=[('Primeiro','Primeiro'),('Segundo','Segundo')])
    ano = StringField('Ano da Avaliacao(AAAA)')
    numerodeQuestoes = StringField('Numero de questoes desejado')
    vezesUsadas = StringField('Numero de uso das questoes')
    submit = SubmitField('Cadastrar')


class ListarAvaliacaoForm(FlaskForm):
    disciplinas = SelectField('Nome da Disciplina',coerce=int)
    semestre = SelectField('Semestre da Avaliacao',choices=[('Primeiro','Primeiro'),('Segundo','Segundo')])
    ano = StringField('Digite o ano(AAAA) exato das avaliacoes a consultar')
    avaliacoes = SelectField('Nome da Avaliacao')
    submitListar = SubmitField('Listar Avaliacoes')
    submitEditar = SubmitField('Editar Avaliacao')
    submitExcluir = SubmitField('Excluir Avaliacao')

class EditarAvaliacaoForm(FlaskForm):
    avaliacao = StringField('Nome atual da avaliacao')
    semestre = StringField('Semestre atual da avaliacao')
    ano = StringField('Ano atual da avaliacao')
    novaAvaliacao = StringField('Digite o novo nome da avaliacao')
    novoSemestre = SelectField('Selecione o novo semestre da Avaliacao', choices=[('Primeiro', 'Primeiro'), ('Segundo', 'Segundo')])
    novoAno = StringField('Digite o novo ano da avaliacao')
    submit = SubmitField('Editar')





