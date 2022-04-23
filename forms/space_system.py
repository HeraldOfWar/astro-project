from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SpaceSystemForm(FlaskForm):
    """Форма для создания/изменения звёздной системы"""
    name = StringField('Название', validators=[DataRequired()])
    galaxy = StringField("Галактика")
    about = TextAreaField('Описание')
    submit = SubmitField('Добавить')
