from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.space_systems import SpaceSystem
from data.parsers import space_system_parser


class SpaceSystemsResource(Resource):
    """Ресурс звёздной системы (restful-api)"""

    def get(self, space_system_id):
        """Получение звёздной системы"""
        abort_if_space_system_not_found(space_system_id)
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        return jsonify(
            {
                'space_system':
                    space_system.to_dict(
                        only=(
                            'name', 'galaxy', 'about', 'user.name'))
            }
        )

    def post(self, space_system_id):
        """Изменение звёздной системы"""
        abort_if_space_system_not_found(space_system_id)
        args = space_system_parser.parse_args()
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        space_system.name = args['name']
        space_system.galaxy = args['galaxy']
        space_system.about = args['about']
        space_system.creator = args['creator']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, space_system_id):
        """Удаление звёздной системы"""
        abort_if_space_system_not_found(space_system_id)
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        session.delete(space_system)
        session.commit()
        return jsonify({'success': 'OK'})


class SpaceSystemsListResource(Resource):
    """Ресурс списка звёздных систем (restful-api)"""

    def get(self):
        """Получение всех звёздных систем"""
        session = db_session.create_session()
        space_systems = session.query(SpaceSystem).all()
        return jsonify(
            {
                'space_systems':
                    [item.to_dict(
                        only=(
                            'name', 'galaxy', 'about', 'user.name'))
                        for item in space_systems]
            }
        )

    def post(self):
        """Создание звёздной системы"""
        args = space_system_parser.parse_args()
        session = db_session.create_session()
        space_system = SpaceSystem(
            name=args['name'],
            space_type=args['galaxy'],
            about=args['about'],
            creator=args['creator']
        )
        session.add(space_system)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_space_system_not_found(space_system_id):
    """Обработка ситуации, когда звёздной системы с указанным id не существует"""
    session = db_session.create_session()
    space_system = session.query(SpaceSystem).get(space_system_id)
    if not space_system:
        abort(404, message=f"Space system {space_system_id} not found")
