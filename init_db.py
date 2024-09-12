from config import app, db
from models import User, Event, Task

# Cria todas as tabelas definidas nos modelos
with app.app_context():
    db.create_all()
    print("Banco de dados e tabelas criados/atualizados com sucesso.")
