import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class SpaceObject(SqlAlchemyBase, SerializerMixin):
    """Модель космического объекта"""
    __tablename__ = 'space_objects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)  # название объекта
    space_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # тип объекта
    radius = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # расстояние до Звезды
    period = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # период обращения вокруг Звезды
    ex = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # эксцентриситет
    v = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # орбитальная скорость
    p = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # плотность поверхности
    g = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # ускорение свободного падения
    m = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # масса
    sputnik = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # количество спутников
    atmosphere = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # описание атмосферы
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # общее описание
    image_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # путь к изображению объекта
    system = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("space_systems.id"))  # id системы, в которой находится объект
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))  # id создателя объекта
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания объекта
    user = orm.relation('User')  # связываем с моделью пользователя
    space_system = orm.relation('SpaceSystem')  # связываем с модель системы

    def __repr__(self):
        return f'<SpaceObject> {self.name}'
