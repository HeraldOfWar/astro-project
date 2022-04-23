import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class News(SqlAlchemyBase, SerializerMixin):
    """Модель записи пользователя"""
    __tablename__ = 'news'  # название таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)  # идентификатор
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # заголовок
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # содержимое (текст)
    photo_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # путь к изображению
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)  # дата создания
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)  # личное/публичное
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))  # идентификатор автора записи
    user = orm.relation('User')  # связываем с моделью пользователя

    def __repr__(self):
        return f'<News> {self.title}'
    