import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class SpaceSystem(SqlAlchemyBase, SerializerMixin):
    """Модель звёздной системы"""
    __tablename__ = 'space_systems'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)  # название звёздной системы
    galaxy = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # название галактики, в которой находится система
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # описание звёздной системы
    creator = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))  # id создателя звёздной системы
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания звёздной системы
    user = orm.relation('User')  # связываем с моделью пользователя
    space_objects = orm.relation('SpaceObject',
                                 back_populates='space_system')  # связываем с моделью космического объекта

    def __repr__(self):
        return f'<SpaceSystem> {self.name}'
