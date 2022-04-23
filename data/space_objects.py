import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase


class SpaceObject(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'space_objects'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    space_type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    radius = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    period = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    ex = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    v = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    p = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    g = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    m = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sputnik = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    atmosphere = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    system = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("space_systems.id"))
    creator = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user = orm.relation('User')
    space_system = orm.relation('SpaceSystem')

    def __repr__(self):
        return f'<SpaceObject> {self.name}'
