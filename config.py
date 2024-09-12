from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Criação da aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados e chave secreta
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event_manager.db'

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Inicialização do LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Carregamento do usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importar modelos após a inicialização
from models import User, Task, Event
