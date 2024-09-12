from flask import render_template, redirect, url_for, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from config import app, db
from models import User, Event, Task
from forms import RegisterForm, LoginForm, EventForm, TaskForm
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    formulario = RegisterForm()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        sen = generate_password_hash(formulario.password.data)

        usuBanco = User.query.filter_by(usuario=usu).first()
        if usuBanco:
            print('Usuário já existe')
        else:
            novoUsuario = User(usuario=usu, senha=sen)
            db.session.add(novoUsuario)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', form=formulario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = LoginForm()

    if formulario.validate_on_submit():
        usu = formulario.username.data
        usuBanco = User.query.filter_by(usuario=usu).first()

        if usuBanco:
            sen = formulario.password.data
            senhaHash = usuBanco.senha

            if check_password_hash(senhaHash, sen):
                login_user(usuBanco)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=formulario)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    meus_eventos = Event.query.filter_by(user_id=current_user.id).all()
    minhas_tarefas = Task.query.filter_by(user_id=current_user.id).all()  # Adicionei isso para as tarefas
    return render_template('dashboard.html', todos_eventos=meus_eventos, minhas_tarefas=minhas_tarefas)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            nome=form.event_name.data,
            data_evento=form.event_date.data,
            descricao=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_event.html', form=form)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        event.nome = form.event_name.data
        event.data_evento = form.event_date.data
        event.descricao = form.description.data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_event.html', form=form, event=event)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            title=form.title.data,
            data_evento=form.event_date.data,
            description=form.description.data,
            status=form.status.data,  # Adiciona o status
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_task.html', form=form)

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data  # Atualiza o status
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', form=form, task=task)

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
