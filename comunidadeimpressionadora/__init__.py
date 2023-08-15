from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '5273daab6707d37d347f76a95535f1f5'
#bcrypt para crptografar as senhas do site
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u'Faça login para ter acesso a está área.'
login_manager.login_message_category = 'alert-info'
from comunidadeimpressionadora import routes
