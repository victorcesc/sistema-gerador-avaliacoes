import random

from flask import render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link
from werkzeug.utils import redirect

from forms import *
from models import *

boostrap = Bootstrap(app) # isso habilita o template bootstrap/base.html
nav = Nav()
nav.init_app(app) # isso habilita a criação de menus de navegação do pacote Flask-Nav


@nav.navigation()
def meunavbar():
    menu = Navbar('Minha aplicação')
    menu.items = [View('Home', 'inicio')]

    if session.get('logged_in') is True:
        menu.items.append(Subgroup('Disciplina', View('Cadastro de Disciplina', 'cadastroDisciplina'), View('Listar Disciplina', 'listarDisciplina')))
        menu.items.append(Subgroup('Assunto', View('Cadastro de Assuntos', 'cadastroAssunto'), View('Listar Assuntos', 'listarAssunto')))
        menu.items.append(Subgroup('Questoes', View('Cadastro de Questoes', 'cadastroQuestao'), View('Listar Questoes', 'listarQuestao')))
        menu.items.append(Subgroup('Alternativas', View('Cadastro de Alternativas', 'cadastroAlternativa'), View('Listar Alternativas', 'listarAlternativa')))
        menu.items.append(Subgroup('Avaliacoes', View('Cadastro de Avaliacoes', 'cadastroAvaliacao'), View('Listar Avaliacoes', 'listarAvaliacao')))


        menu.items.append(View('Sair','sair'))
    else:
        menu.items.append(View('Login', 'autenticar'))
        menu.items.append(View('Registrar','cadastro'))
        menu.items.append(Link('Ajuda','https://www.google.com'))
    return menu


@app.route('/registro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        usuarioLogin = form.username.data
        usuarioPassword = form.password.data



        if Usuario.query.filter_by(login=form.username.data).first() != None:
            flash("O username {} já existe, digite outro".format(usuarioLogin), 'error')
        else:
            novo_usuario = Usuario(login=usuarioLogin, senha=usuarioPassword)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário {} criado com sucesso'.format(usuarioLogin))
        return render_template('index.html', title="Usuário registrado")
    else:
        return render_template('registro.html', title='Cadastro de usuário', form=form)


@app.route('/login', methods=['GET', 'POST'])
def autenticar():
    form = LoginForm()

    if form.validate_on_submit():

        # Veja mais em: http://flask-sqlalchemy.pocoo.org/2.3/queries/#querying-records
        usuario = Usuario.query.filter_by(login=form.username.data).first_or_404()

        if (usuario.check_password(form.password.data)):
            session['logged_in'] = True
            session['idUsuario'] = usuario.get_idUsuario()
            flash('Bem vindo {}'.format(usuario.login))
            return render_template('autenticado.html', title="Usuário autenticado",usuario=usuario.get_idUsuario())
        else:
            flash('Usuário ou senha inválidos')
            return render_template('login.html', title='Autenticação de usuários', form=form)

    else:
        return render_template('login.html', title='Autenticação de usuários', form=form)


#@app.route('/disciplina')
#def cadastrarDisciplina():







@app.route('/cadastroDisciplina',methods=['GET','POST'])
def cadastroDisciplina():

    form = CadastroDisciplinaForm()

    if form.validate_on_submit():

        nomeDisciplina = form.nomeDisciplina.data

        if Disciplina.query.filter_by(nomeDisciplina=nomeDisciplina,idUsuario=session.get('idUsuario'),statusDisc='ativo').first() != None:
            flash('A disciplina {} ja existe, digite outra'.format(nomeDisciplina),'error')
            return render_template('registro.html',title='Cadastro Disciplina',form=form)
        else:
            nova_disciplina = Disciplina(nomeDisciplina=nomeDisciplina)
            db.session.add(nova_disciplina)
            db.session.commit()
            flash('Disciplina {} criada com sucesso'.format(nomeDisciplina))
            return render_template('registro.html',title='Cadastro Disciplina',form=form)

    return render_template('registro.html', title='Cadastro de disciplina', form=form)



@app.route('/listarDisciplina',methods=['GET','POST'])
def listarDisciplina():
    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = ListarDisciplinasForm()
    form.disciplinas.choices = listadF

    if form.disciplinas.data != None:
        if form.submitExcluir.data:

            idDisciplina = form.disciplinas.data
            disciplina = Disciplina.query.filter_by(idDisciplina=idDisciplina, statusDisc='ativo').first()

            disciplina.desativarDisciplina()
            db.session.commit()
            flash('Disciplina excluida com sucesso')
            return render_template('listarDisciplina.html', title='Listar Disciplinas', form=form)

        if form.submitEditar.data:
            idDisciplina = form.disciplinas.data
            return redirect(url_for('editarDisciplina', idDisciplina=idDisciplina))


    return render_template('listarDisciplina.html', title='Listar Disciplinas', form=form)



@app.route('/editarDisciplina', methods=['GET', 'POST'])
def editarDisciplina():
    if session.get('logged_in') is False:
        return inicio()

    idDisciplina = str(request.args.get('idDisciplina'))

    disciplina = Disciplina.query.filter_by(idDisciplina=idDisciplina).first()

    if disciplina is None:
        flash('Selecione uma disciplina')
        return redirect(url_for('listarDisciplina'))
    form = EditarDisciplinaForm(nomeDisciplina=disciplina.get_nomeDisciplina())

    if request.method == 'GET':
        # pegar o id da pessoa via GET (parâmetro id na URL)
        if int(disciplina.get_idUsuario()) != session['idUsuario']:
            return inicio()

        if disciplina is None:
            return redirect(url_for('listarDisciplinas'))
        return render_template('editar.html', title='Editar disciplina', form=form, disciplina=disciplina)
    else:
        novaDisciplina = form.novaDisciplina.data
        if novaDisciplina == disciplina.get_nomeDisciplina():
            flash("Digite um nome diferente pra disciplina", 'error')

            return render_template('editar.html', title='Editar disciplina', form=form, disciplina=disciplina)
        else:
            if Disciplina.query.filter_by(nomeDisciplina=novaDisciplina,statusDisc='ativo',
                                          idUsuario=session.get('idUsuario')).first() != None:
                flash("A disciplina {} já existe".format(novaDisciplina), 'error')
                return render_template('editar.html', title='Editar disciplina', form=form, disciplina=disciplina)

        disciplina.set_nomeDisciplina(novaDisciplina)
        db.session.commit()

        flash("Disciplina alterada com sucesso!")
    return render_template('editar.html', title='Editar disciplina', form=form, disciplina=disciplina)






@app.route('/cadastroAssunto',methods=['GET', 'POST'])
def cadastroAssunto():

    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina , Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = CadastroAssuntoForm()
    form.disciplinas.choices = listadF


    if form.validate_on_submit():

        nomeAssunto = form.nomeAssunto.data
        idDisciplina = form.disciplinas.data

        if Assunto.query.filter_by(nomeAssunto=nomeAssunto,statusAss='ativo',idDisciplina=idDisciplina).first()!=None:
            flash('O assunto {} para a disciplina selecionada ja existe, digite outro'.format(nomeAssunto), 'error')
            return render_template('cadastroAssunto.html',title='Cadastro de Assunto',disciplinas=listaD,form=form)
        else:
            novo_assunto = Assunto(nomeAssunto=nomeAssunto,idDisciplina=idDisciplina)
            db.session.add(novo_assunto)
            db.session.commit()
            flash('Assunto {} criado com sucesso'.format(form.nomeAssunto.data))
            return render_template('cadastroAssunto.html', title='Cadastro de Assunto', disciplinas=listaD, form=form)

    return render_template('cadastroAssunto.html', title='Cadastro de Assunto', disciplinas=listaD,form=form)


@app.route('/listarAssunto',methods=['GET','POST'])
def listarAssunto():
    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = ListarAssuntoForm()
    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data
    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina, statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto, Assunto.nomeAssunto) for Assunto in listaA]
    form.assuntos.choices = listaAf



    if form.validate_on_submit():
            if form.submit2.data and form.assuntos.choices!=None:
                idAssunto = form.assuntos.data
                assunto = Assunto.query.filter_by(idAssunto=idAssunto,statusAss='ativo').first()

                assunto.desativarAssunto()

                db.session.commit()
                flash("Assunto excluído com sucesso!")
                return redirect(url_for('listarAssunto'))

            if form.submit3.data and form.assuntos.choices!=None:
                idAssunto = form.assuntos.data
                return redirect(url_for('editarAssunto',idAssunto=idAssunto))



    return render_template('listarAssunto.html',nomeColuna= 'Assuntos',title='Listar Assuntos',form=form)



@app.route('/editarAssunto',methods=['GET','POST'])
def editarAssunto():
    if session.get('logged_in') is False:
        return inicio()

    idAssunto = str(request.args.get('idAssunto'))
    assunto = Assunto.query.filter_by(idAssunto=idAssunto).first()
    form = EditarAssuntoForm(nomeAssunto=assunto.get_nomeAssunto())



    if request.method == 'GET':
        # pegar o id da pessoa via GET (parâmetro id na URL)


        if assunto is None:
            return redirect(url_for('listarAssuntos'))
        return render_template('editarAssunto.html', title='Editar assunto', form=form)
    else:
        novoAssunto = form.novoAssunto.data
        if novoAssunto == assunto.get_nomeAssunto():
            flash("Digite um nome diferente pro Assunto", 'error')
            return render_template('editarAssunto.html',title='Editar Assunto',form=form)
        else:
            if Assunto.query.filter_by(nomeAssunto=novoAssunto,statusAss='ativo',idDisciplina=assunto.idDisciplina).first() != None:
                flash("O assunto {} já existe".format(novoAssunto), 'error')
                return render_template('editarAssunto.html', title='Editar Assunto', form=form)


        assunto.set_nomeAssunto(novoAssunto)
        db.session.commit()

        flash("Assunto alterado com sucesso!")
    return render_template('editarAssunto.html', title='Editar Assunto', form=form)



@app.route('/cadastroQuestao',methods=['GET','POST'])
def cadastroQuestao():


    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = CadastroQuestaoForm()
    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data

    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina, statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto, Assunto.nomeAssunto) for Assunto in listaA]
    form.assuntos.choices = listaAf

    idAssunto = form.assuntos.data


    if form.submitCadastro.data:
        if form.pergunta.data!='' and form.resposta.data!='' and idAssunto!=None:
            pergunta = form.pergunta.data
            resposta = form.resposta.data
            tipo = form.tipo.data
            if Questao.query.filter_by(idAssunto=idAssunto,pergunta=pergunta,resposta=resposta,tipo=tipo,statusQ='ativo').first()!=None:
                flash('A questao {} ja existe'.format(pergunta))
                return render_template('cadastroQuestao.html',title='Cadastro de Questao',form=form)
            else:
                nova_questao = Questao(idAssunto=idAssunto,pergunta=pergunta,resposta=resposta,tipo=tipo,vezesUsada=0,statusQ='ativo')
                db.session.add(nova_questao)
                db.session.commit()
                flash('Questao " {} " cadastrada com sucesso'.format(nova_questao.get_pergunta()))
                return render_template('cadastroQuestao.html',title='Cadastro de Questao',form=form)
        else:
            flash('Preencha todos os campos!')
            return render_template('cadastroQuestao.html',title='Cadastro de Questao',form=form)
    return render_template('cadastroQuestao.html',title='Cadastro de Questao',form=form)



@app.route('/listarQuestao',methods=['GET','POST'])
def listarQuestao():

    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = ListarQuestaoForm()

    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data

    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina, statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto, Assunto.nomeAssunto) for Assunto in listaA]

    form.assuntos.choices = listaAf

    idAssunto = form.assuntos.data

    listaQ = Questao.query.filter_by(idAssunto=idAssunto,statusQ='ativo').all()
    listaQf = [(Questao.idQuestao,Questao.pergunta) for Questao in listaQ]
    form.questoes.choices = listaQf





    if form.questoes.data!=None:
        if form.submitExcluir.data:
            idQuestao = form.questoes.data
            questao = Questao.query.filter_by(idQuestao=idQuestao, statusQ='ativo').first()

            questao.desativarQuestao()

            db.session.commit()
            flash('Questao excluida com sucesso')
            return render_template('listarQuestao.html', title='Listar Questoes', form=form)

        if form.submitEditar.data:
            idQuestao = form.questoes.data
            return redirect(url_for('editarQuestao', idQuestao=idQuestao))


    return render_template('listarQuestao.html', title='Listar Questoes', form=form)


@app.route('/editarQuestao',methods=['GET','POST'])
def editarQuestao():

    idQuestao = str(request.args.get('idQuestao'))
    questao = Questao.query.filter_by(idQuestao=idQuestao).first()
    form = EditarQuestaoForm(pergunta= questao.get_pergunta(),tipo=questao.get_tipo())

    if request.method == 'GET':

        if questao is None:
            return redirect(url_for('listarQuestao'))
        return render_template('editarQuestao.html', title='Editar Questao', form=form)
    else:
        novaPergunta = form.nova_pergunta.data
        novaResposta = form.nova_resposta.data
        tipo = form.novo_tipo.data
        if novaPergunta == questao.get_pergunta() and novaResposta == questao.get_resposta():
            flash("Digite um nome diferente para a Questao", 'error')
            return render_template('editarQuestao.html', title='Editar Questao', form=form)
        else:
            if Questao.query.filter_by(pergunta=novaPergunta,resposta=novaResposta, statusQ='ativo',
                                   idAssunto=questao.idAssunto).first() != None:
                flash('A questao "{}" já existe'.format(novaPergunta), 'error')
                return render_template('editarQuestao.html', title='Editar Questao', form=form)
        questao.set_pergunta(novaPergunta)
        questao.set_resposta(novaResposta)
        questao.set_tipo(tipo)
        db.session.commit()
        flash("Questao alterada com sucesso!")

    return render_template('editarQuestao.html',form=form)

@app.route('/cadastroAlternativa',methods=['GET','POST'])
def cadastroAlternativa():
    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = CadastroAlternativaForm()

    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data

    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina, statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto, Assunto.nomeAssunto) for Assunto in listaA]

    form.assuntos.choices = listaAf

    idAssunto = form.assuntos.data

    listaQ = Questao.query.filter_by(idAssunto=idAssunto,tipo='Multipla Escolha', statusQ='ativo').all()
    listaQf = [(Questao.idQuestao, Questao.pergunta) for Questao in listaQ]
    form.questoes.choices = listaQf
    idQuestao = form.questoes.data


    if form.submitCadastro.data:
            if form.disciplinas.data!= None and form.questoes.data != None:
                alternativa = form.alternativa.data
                if Alternativas.query.filter_by(idAssunto=idAssunto,idQuestao=idQuestao, alternativa=alternativa,
                                           statusAl='ativo').first() != None:
                    flash('A alternativa {} ja existe'.format(alternativa))
                    return render_template('cadastroAlternativa.html', title='Cadastro de Alternativas', form=form)
                else:
                    nova_alternativa = Alternativas(idAssunto=idAssunto,idQuestao=idQuestao,alternativa=alternativa, statusAl='ativo')
                    db.session.add(nova_alternativa)
                    db.session.commit()
                    flash('Alternativa " {} " cadastrada com sucesso'.format(nova_alternativa.get_alternativa()))
                    return render_template('cadastroAlternativa.html', title='Cadastro de Alternativas', form=form)
            else:
                flash('Preencha todos os campos!')
                return render_template('cadastroAlternativa.html', title='Cadastro de Alternativas', form=form)
    return render_template('cadastroAlternativa.html',title='Cadastro de Alternativas',form=form)





@app.route('/listarAlternativa', methods=['GET','POST'])
def listarAlternativa():
    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = ListarAlternativaForm()

    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data

    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina, statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto, Assunto.nomeAssunto) for Assunto in listaA]

    form.assuntos.choices = listaAf

    idAssunto = form.assuntos.data

    listaQ = Questao.query.filter_by(idAssunto=idAssunto, tipo='Multipla Escolha', statusQ='ativo').all()
    listaQf = [(Questao.idQuestao, Questao.pergunta) for Questao in listaQ]
    form.questoes.choices = listaQf
    idQuestao = form.questoes.data

    listaAl = Alternativas.query.filter_by(idAssunto=idAssunto,idQuestao=idQuestao,statusAl='ativo').all()
    listaAlf = [(Alternativas.idAlternativas, Alternativas.alternativa) for Alternativas in listaAl]
    form.alternativas.choices = listaAlf


    if form.alternativas.data != None:
        if form.submitExcluir.data:
            idAlternativas = form.alternativas.data
            alternativa = Alternativas.query.filter_by(idAlternativas=idAlternativas, statusAl='ativo').first()
            alternativa.desativarAlternativa()
            db.session.commit()
            flash('Alternativa excluida com sucesso')
            return render_template('listarAlternativa.html', title='Listar Alternativas', form=form)

        if form.submitEditar.data:
            idAlternativas = form.alternativas.data
            return redirect(url_for('editarAlternativa', idAlternativas=idAlternativas))

    return render_template('listarAlternativa.html', title='Listar Alternativa', form=form)







@app.route('/editarAlternativa',methods=['GET','POST'])
def editarAlternativa():

    idAlternativas = str(request.args.get('idAlternativas'))
    alternativa = Alternativas.query.filter_by(idAlternativas=idAlternativas,statusAl='ativo').first()

    form = EditarAlternativaForm(alternativa=alternativa.get_alternativa())

    if request.method == 'GET':

        if alternativa is None:
            return redirect(url_for('listarAlternativa'))
        return render_template('editarAlternativa.html', title='Editar Alternativa', form=form)
    else:
        novaAlternativa = form.nova_alternativa.data
        if novaAlternativa== alternativa.get_alternativa():
            flash("Digite um nome diferente pra Alternativa", 'error')
            return render_template('editarAlternativa.html', title='Editar Alternativa', form=form)
        else:
            if Alternativas.query.filter_by(alternativa=novaAlternativa, idQuestao=str(alternativa.get_idQuestao), idAssunto=str(alternativa.get_idAssunto), statusAl='ativo').first() != None:
                flash('A alternativa "{}" já existe'.format(novaAlternativa), 'error')
                return render_template('editarAlternativa.html', title='Editar Alternativa', form=form)
        alternativa.set_alternativa(novaAlternativa)
        db.session.commit()
        flash("Alternativa alterada com sucesso!")




    return redirect(url_for('listarAlternativa'))




@app.route('/cadastroAvaliacao',methods=['GET','POST'])
def cadastroAvaliacao():
    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina, Disciplina.nomeDisciplina) for Disciplina in listaD]
    form = CadastroAvaliacaoForm()
    form.disciplinas.choices = listadF

    idDisciplina = form.disciplinas.data

    listaA = Assunto.query.filter_by(idDisciplina=idDisciplina,statusAss='ativo').all()
    listaAf = [(Assunto.idAssunto) for Assunto in listaA]

    if form.is_submitted():
        if form.nomeAvaliacao.data!='' and form.semestre.data!='' and form.ano.data!='' and form.numerodeQuestoes!='' and form.vezesUsadas.data != '' and form.disciplinas.data!=None and len(listaAf)!=0:
            semestre = form.semestre.data
            ano = form.ano.data
            numerodeQuestoes = form.numerodeQuestoes.data
            vezesUsadas = form.vezesUsadas.data

            nova_avaliacao = form.nomeAvaliacao.data
            if Avaliacao.query.filter_by(idDisciplina=idDisciplina, nomeAvaliacao=nova_avaliacao,statusAv='ativo',semestre=semestre,ano=ano).first() != None:
                flash('A avaliacao "{}" ja existe.'.format(nova_avaliacao),'error')
                return render_template('cadastroAvaliacao.html', title='Cadastro de Avaliacoes', form=form)
            else:
                vetorL = list()
                for idAssunto in listaAf:
                    listaQ = Questao.query.filter_by(idAssunto=idAssunto,vezesUsada=int(vezesUsadas),statusQ='ativo').all()
                    listaQf = [(Questao.idQuestao) for Questao in listaQ]
                    for idQuestao in listaQf:
                        vetorL.append(idQuestao)

                if(len(vetorL)!=0):

                    new_av = Avaliacao(nomeAvaliacao=nova_avaliacao,statusAv='ativo',idDisciplina=idDisciplina,semestre=semestre,ano=ano,numerodeQuestoes=numerodeQuestoes)
                    db.session.add(new_av)
                    db.session.commit()
                    if int(numerodeQuestoes)>len(vetorL) or int(numerodeQuestoes)==len(vetorL):

                        for idQuestao in vetorL:
                            q_add_vezes = Questao.query.filter_by(idQuestao=idQuestao,statusQ='ativo').first()
                            q_add_vezes.plusvezesUsada()
                            nova_av_q = AvaliacoesQuestao(idAvaliacao=new_av.idAvaliacao,idQuestao=idQuestao)
                            db.session.add(nova_av_q)
                            db.session.commit()
                        flash('Foram adicionadas {} Questoes que respeitam os requesitos a Avaliacao'.format(len(vetorL)))

                        return render_template('cadastroAvaliacao.html', title='Cadastro de Avaliacoes', form=form)

                    if int(numerodeQuestoes)<len(vetorL):
                        i=0
                        naoRepetir = list()
                        while(i<int(numerodeQuestoes)):
                            idQuestao = random.choice(vetorL)
                            if idQuestao not in naoRepetir:
                                naoRepetir.append(idQuestao)
                                q_add_vezes = Questao.query.filter_by(idQuestao=idQuestao, statusQ='ativo').first()
                                q_add_vezes.plusvezesUsada()
                                nova_av_q = AvaliacoesQuestao(idAvaliacao=new_av.idAvaliacao,idQuestao=idQuestao)
                                db.session.add(nova_av_q)
                                db.session.commit()
                            i+=1
                        flash('Foram adicionadas {} Questoes a Avaliacao'.format(numerodeQuestoes))

                        return render_template('cadastroAvaliacao.html', title='Cadastro de Avaliacoes', form=form)
                else:
                    flash('Nao há questoes cadastradas ou nao saciam os requisitos para adicionar em uma avaliacao')
                    return render_template('cadastroAvaliacao.html', title='Cadastro de Avaliacoes', form=form)
        else:
            flash('É necessario preencher todos os campos')
            return render_template('cadastroAvaliacao.html', title='Cadastro de Avaliacoes', form=form)

    return render_template('cadastroAvaliacao.html',title = 'Cadastro de Avaliacoes',form=form)

@app.route('/listarAvaliacao',methods=['GET','POST'])
def listarAvaliacao():

    form = ListarAvaliacaoForm()

    listaD = Disciplina.query.filter_by(idUsuario=session.get('idUsuario'), statusDisc='ativo').all()
    listadF = [(Disciplina.idDisciplina , Disciplina.nomeDisciplina) for Disciplina in listaD]
    form.disciplinas.choices = listadF
    idDisciplina = form.disciplinas.data
    semestre = form.semestre.data
    ano = form.ano.data


    listaAv = Avaliacao.query.filter_by(idDisciplina=idDisciplina,semestre=semestre,ano=ano,statusAv='ativo')
    listaAvf = [(Avaliacao.idAvaliacao, Avaliacao.nomeAvaliacao) for Avaliacao in listaAv]

    form.avaliacoes.choices = listaAvf

    print('idAvaliacao = {}'.format(form.avaliacoes.data))

    if form.avaliacoes.data != None:

        if form.submitExcluir.data:
            idAvaliacao = form.avaliacoes.data
            avaliacao = Avaliacao.query.filter_by(idAvaliacao=idAvaliacao, statusAv='ativo').first()
            avaliacao.desativarAvaliacao()
            db.session.commit()
            flash('Avaliacao excluida com sucesso')
            return render_template('listarAvaliacao.html', title='Listar Avaliacoes', form=form)

        if form.submitEditar.data:
            idAvaliacao = form.avaliacoes.data
            return redirect(url_for('editarAvaliacao', idAvaliacao=idAvaliacao))
    else:
        flash('Nao há avaliacao selecionada')
        return render_template('listarAvaliacao.html', title='Listar Avaliacoes', form=form)

    return render_template('listarAvaliacao.html', title='Listar Avaliacoes', form=form)




@app.route('/editarAvaliacao',methods=['GET','POST'])
def editarAvaliacao():
    idAvaliacao = str(request.args.get('idAvaliacao'))
    avaliacao = Avaliacao.query.filter_by(idAvaliacao=idAvaliacao,statusAv='ativo').first()

    if avaliacao is None:
        flash('Selecione uma avaliacao')
        return redirect(url_for('listarAvaliacao'))

    form = EditarAvaliacaoForm(avaliacao=avaliacao.get_nomeAvaliacao(),semestre=avaliacao.get_semestre(),ano=avaliacao.get_ano())

    if request.method == 'GET':

        if avaliacao is None:
            return redirect(url_for('listarAvaliacao'))
        return render_template('editarAlternativa.html', title='Editar Alternativa', form=form)
    else:
        nomeAvaliacao = form.novaAvaliacao.data
        novoSemestre = form.novoSemestre.data
        novoAno = form.novoAno.data
        if nomeAvaliacao == avaliacao.get_nomeAvaliacao() and novoSemestre == avaliacao.get_semestre() and novoAno == avaliacao.get_ano() :
            flash("Digite valores diferentes pra Avaliacao", 'error')
            return render_template('editarAvaliacao.html', title='Editar Avaliacao', form=form)
        else:
            if Avaliacao.query.filter_by(nomeAvaliacao=nomeAvaliacao, idDisciplina=avaliacao.idDisciplina,
                                            semestre=novoSemestre,ano=novoAno, statusAv='ativo').first() != None:
                flash('A avaliacao "{}" já existe'.format(nomeAvaliacao), 'error')
                return render_template('editarAvaliacao.html', title='Editar Avaliacao', form=form)
        avaliacao.set_nomeAvaliacao(nomeAvaliacao)
        avaliacao.set_ano(novoAno)
        avaliacao.set_semestre(novoSemestre)
        db.session.commit()
        flash("Avaliacao alterada com sucesso!")

    return render_template('editarAvaliacao.html', title='Editar Avaliacao', form=form)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/aluno')
def aluno():
    '''
    Ilustra um exemplo de como exibir tabelas. Também mostrado um exemplo do flask-bootstrap-table
    As estuturas de dados 'data'e 'columns' estão no script dadostabela.py
    :return:
    '''
    return render_template('alunos.html',data=data,columns=columns)



@app.errorhandler(404)
def page_not_found(e):
    '''
    Para tratar erros de páginas não encontradas - HTTP 404
    :param e:
    :return:
    '''
    return render_template('404.html'), 404


@app.route('/logout')
def sair():
    session['logged_in'] = False
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

