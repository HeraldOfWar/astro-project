from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.space_objects import SpaceObject
from data.parsers import space_object_parser


class SpaceObjectsResource(Resource):
    """Ресурс космического объекта (restful-api)"""

    def get(self, space_object_id):
        """Получение космического объекта"""
        abort_if_space_object_not_found(space_object_id)
        session = db_session.create_session()
        space_object = session.query(SpaceObject).get(space_object_id)
        return jsonify(
            {
                'space_object':
                    space_object.to_dict(
                        only=(
                            'name', 'space_type', 'radius', 'period', 'ex', 'v', 'p', 'g',
                            'm', 'sputnik', 'atmosphere', 'about', 'user.name', 'image_path'))
            }
        )

    def post(self, space_object_id):
        """Изменение космического объекта"""
        abort_if_space_object_not_found(space_object_id)
        args = space_object_parser.parse_args()
        session = db_session.create_session()
        space_object = session.query(SpaceObject).get(space_object_id)
        space_object.name = args['name']
        space_object.space_type = args['space_type']
        space_object.radius = args['radius']
        space_object.period = args['period']
        space_object.ex = args['ex']
        space_object.v = args['v']
        space_object.p = args['p']
        space_object.g = args['g']
        space_object.m = args['m']
        space_object.sputnik = args['sputnik']
        space_object.atmosphere = args['atmosphere']
        space_object.about = args['about']
        space_object.creator = args['creator']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, space_object_id):
        """Удаление космического объекта"""
        abort_if_space_object_not_found(space_object_id)
        session = db_session.create_session()
        space_object = session.query(SpaceObject).get(space_object_id)
        session.delete(space_object)
        session.commit()
        return jsonify({'success': 'OK'})


class SpaceObjectsListResource(Resource):
    """Ресурс списка космических объектов (restful-api)"""

    def get(self):
        """Получение всех космических объектов"""
        session = db_session.create_session()
        space_objects = session.query(SpaceObject).all()
        return jsonify(
            {
                'space_objects':
                    [item.to_dict(
                        only=(
                            'name', 'space_type', 'radius', 'period', 'ex', 'v', 'p', 'g',
                            'm', 'sputnik', 'atmosphere', 'about', 'user.name', 'image_path'))
                        for item in space_objects]
            }
        )

    def post(self):
        """Создание космического объекта"""
        args = space_object_parser.parse_args()
        session = db_session.create_session()
        space_object = SpaceObject(
            name=args['name'],
            space_type=args['space_type'],
            radius=args['radius'],
            period=args['period'],
            ex=args['ex'],
            v=args['v'],
            p=args['p'],
            g=args['g'],
            m=args['m'],
            sputnik=args['sputnik'],
            atmosphere=args['atmosphere'],
            about=args['about'],
            creator=args['creator']
        )
        session.add(space_object)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_space_object_not_found(space_object_id):
    """Обработка ситуации, когда космического объекта с указанным id не существует"""
    session = db_session.create_session()
    space_object = session.query(SpaceObject).get(space_object_id)
    if not space_object:
        abort(404, message=f"Space object {space_object_id} not found")
