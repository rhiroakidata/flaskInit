from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Projeto
from dao import FuncionarioDao, ProjetoDao
import time
from helpers import deleta_arquivo, recupera_imagem
from mitech import db, app

projeto_dao = ProjetoDao(db)
funcionario_dao = FuncionarioDao(db)


@app.route('/')
def index():
    lista = projeto_dao.listar()
    return render_template('lista.html', titulo='Projetos', projetos=lista)


@app.route('/novo')
def novo():
    if 'funcionario_logado' not in session or session['funcionario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Projeto')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    descricao = request.form['descricao']
    projeto = Projeto(nome, categoria, descricao)
    projeto = projeto_dao.salvar(projeto)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{projeto.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'funcionario_logado' not in session or session['funcionario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    projeto = projeto_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Projeto', projeto=projeto
                           , capa_projeto=nome_imagem or 'capa_padrao.jpg')

@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    descricao = request.form['descricao']
    projeto = Projeto(nome, categoria, descricao, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(projeto.id)
    arquivo.save(f'{upload_path}/capa{projeto.id}-{timestamp}.jpg')
    projeto_dao.salvar(projeto)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    projeto_dao.deletar(id)
    flash('O projeto foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    funcionario = funcionario_dao.buscar_por_email(request.form['funcionario'])
    if funcionario:
        if funcionario.senha == request.form['senha']:
            session['funcionario_logado'] = funcionario.email
            flash(funcionario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['funcionario_logado'] = None
    flash('Nenhum funcionário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
