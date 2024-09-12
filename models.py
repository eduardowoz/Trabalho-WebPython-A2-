from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from config import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    events = db.relationship('Event', backref='creator', lazy=True)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    data_evento = db.Column(db.Date, nullable=False)
    descricao = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    data_evento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # Adiciona o campo status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
