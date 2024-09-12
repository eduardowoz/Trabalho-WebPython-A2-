from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EventForm(FlaskForm):
    event_name = StringField('Nome do Evento', validators=[DataRequired()])
    event_date = DateField('Data do Evento', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    description = TextAreaField('Descrição', validators=[DataRequired()])
    submit = SubmitField('Criar Evento')


class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descrição')
    status = SelectField('Status', choices=[('pendente', 'Pendente'), ('em andamento', 'Em Andamento'), ('concluida', 'Concluída')], default='pendente')
    event_date = DateField('Data do Evento', format='%Y-%m-%d', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    submit = SubmitField('Salvar Tarefa')
