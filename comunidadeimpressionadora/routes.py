from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, bcrypt
from comunidadeimpressionadora.formularios import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import session, Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

@app.route("/")
def home():
    posts = session.query(Post).order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route("/contato")
def contato():
    return render_template('contato.html')


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = session.query(Usuario).all()
    return render_template('usuarios.html',lista_usuarios=lista_usuarios)


@app.route("/login",methods=['GET', 'POST'])
def login():
    formulario_login = FormLogin()
    formulario_criarconta = FormCriarConta()

    if formulario_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = session.query(Usuario).filter_by(email=formulario_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,formulario_login.senha.data):
            login_user(usuario,remember=formulario_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email: {formulario_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login. E-mail ou senha incorretos', 'alert-danger')
    if formulario_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(formulario_criarconta.senha.data)
        usuario = Usuario(username=formulario_criarconta.username.data,email=formulario_criarconta.email.data,senha=senha_cript)
        session.add(usuario)
        session.commit()
        session.close()
        flash(f'Conta criada com sucesso para o email: {formulario_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html',formulario_login=formulario_login,formulario_criarconta=formulario_criarconta)


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso','alert-success')

    return redirect(url_for('home'))

@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route("/post/criar", methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        session.add(post)
        session.commit()
        session.close()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    #Este comando do os separa o nome da imagme da extensão dela
    nome, extensao = os.path.splitext(imagem.filename)
    #Comando join concatena os textos separando por barra inversa \
    nome_completo = nome + codigo + extensao
    #Dizendo o local para salvar as imagens
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_completo)

    tamanho = (500, 500)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_completo


def atualizar_cursos(form):
    lista_cursos = ['Não informado']
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    if len(lista_cursos) > 1:
        lista_cursos.pop(0)
    return ';'.join(lista_cursos)

@app.route("/perfil/editar", methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        session.commit()
        flash(f'Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route("/post/<post_id>", methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = session.get(Post,post_id)
    #Lógica de editar post
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            session.commit()
            flash('Post atualizado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route("/post/<post_id>/excluir", methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = session.get(Post,post_id)
    if current_user == post.autor:
        session.delete(post)
        session.commit()
        flash('Post excluído com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)