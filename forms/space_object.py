from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired


class SpaceObjectForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    space_type = StringField('Тип', validators=[DataRequired()])
    radius = FloatField('Расстояние до Звезды (а.е.)')
    period = FloatField('Период обращения вокруг Звезды (в земных годах)')
    ex = FloatField('Эксцентриситет')
    v = FloatField('Орбитальная скорость (км/с)')
    p = FloatField('Плотность (x10^3 кг/м^3)')
    g = FloatField('Ускорение свободного падения (м/с^2)')
    m = FloatField('Масса (в массах Земли)')
    sputnik = IntegerField('Количество спутников')
    atmosphere = TextAreaField('Описание атмосферы (если есть)')
    about = TextAreaField('Общее описание')
    image = FileField('Фото', validators=[FileAllowed(['png', 'jpg', 'jpeg'], 'Только png и jpg!')])
    submit = SubmitField('Добавить')
