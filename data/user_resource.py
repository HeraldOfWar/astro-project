from flask import jsonify, request
from flask_restful import abort, Resource
from . import db_session
from .users import User
from .parsers import user_parser


class UsersResource(Resource):

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user':
                    user.to_dict(
                        only=(
                            'surname', 'name', 'age', 'about', 'email'))
            }
        )

    def post(self, user_id):
        abort_if_user_not_found(user_id)
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['about']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {
                'users':
                    [item.to_dict(
                        only=(
                            'surname', 'name', 'age', 'about', 'email'))
                        for item in users]
            }
        )

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['about'],
            email=args['email']
        )
        user.set_password(request.json['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")