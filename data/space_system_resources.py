from flask import jsonify
from flask_restful import abort, Resource
from data import db_session
from data.space_systems import SpaceSystem
from data.parsers import space_system_parser


class SpaceSystemsResource(Resource):

    def get(self, space_system_id):
        abort_if_space_system_not_found(space_system_id)
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        return jsonify(
            {
                'space_system':
                    space_system.to_dict(
                        only=(
                            'name', 'galaxy', 'user.name'))
            }
        )

    def post(self, space_system_id):
        abort_if_space_system_not_found(space_system_id)
        args = space_system_parser.parse_args()
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        space_system.name = args['name']
        space_system.galaxy = args['galaxy']
        space_system.creator = args['creator']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, space_system_id):
        abort_if_space_system_not_found(space_system_id)
        session = db_session.create_session()
        space_system = session.query(SpaceSystem).get(space_system_id)
        session.delete(space_system)
        session.commit()
        return jsonify({'success': 'OK'})


class SpaceSystemsListResource(Resource):

    def get(self):
        session = db_session.create_session()
        space_systems = session.query(SpaceSystem).all()
        return jsonify(
            {
                'space_systems':
                    [item.to_dict(
                        only=(
                            'name', 'galaxy', 'user.name'))
                        for item in space_systems]
            }
        )

    def post(self):
        args = space_system_parser.parse_args()
        session = db_session.create_session()
        space_system = SpaceSystem(
            name=args['name'],
            space_type=args['galaxy'],
            creator=args['creator']
        )
        session.add(space_system)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_space_system_not_found(space_system_id):
    session = db_session.create_session()
    space_system = session.query(SpaceSystem).get(space_system_id)
    if not space_system:
        abort(404, message=f"Space system {space_system_id} not found")