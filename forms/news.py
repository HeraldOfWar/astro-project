from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    photo = FileField('Фото', validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Только png и jpg!')])
    is_private = BooleanField("Личное")
    submit = SubmitField('Создать')
