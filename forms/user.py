from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms import EmailField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    age = IntegerField('Возраст')
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    login = StringField('Почта/Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EditUserForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст')
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Внести изменения')
