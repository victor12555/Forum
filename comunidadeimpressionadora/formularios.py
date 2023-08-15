from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import session, Usuario
from flask_login import current_user

class FormLogin(FlaskForm):
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer login')

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário',validators=[DataRequired(),Length(6,15)])
    email = StringField('E-mail',validators=[DataRequired(),Email('E-mail inválido')])
    senha = PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha',message='Este campo deve ser igual ao campo da senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

    def validate_email(self, email):
        usuario = session.query(Usuario).filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário',validators=[DataRequired(),Length(6,15)])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'], message='Arquivo não possui uma das extensões aprovadas, JPG ou PNG')])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')
    curso_python = BooleanField('Python Impressionador')
    curso_sql = BooleanField('SQL Impressionador')
    curso_excel = BooleanField('Excel Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')

    def validate_email(self, email):
        #Verificar se o cara mudou de email
        if current_user.email != email.data:
            usuario = session.query(Usuario).filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail.')


class FormCriarPost(FlaskForm):
    titulo =  StringField('Título do Post',validators=[DataRequired(),Length(5,140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')