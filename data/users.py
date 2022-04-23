import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True)  # логин
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # фамилия
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # возраст
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # описание пользователя
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True)  # электронная почта
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # пароль (хэшированный)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания пользователя
    news = orm.relation("News", back_populates='user')  # связываем с модель записи
    space_systems = orm.relation("SpaceSystem", back_populates='user')  # связываем с моделью космического объекта
    space_objects = orm.relation("SpaceObject", back_populates='user')  # связываем с моделью звёздной системы

    def set_password(self, password):
        """Хэширование пароля"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Сравнение хэшей введённого пароля с установленным"""
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User> {self.username}'
