from flask_restful import reqparse

user_parser = reqparse.RequestParser()
user_parser.add_argument('surname', required=True)
user_parser.add_argument('name', required=True)
user_parser.add_argument('age', type=int)
user_parser.add_argument('about')
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)


news_parser = reqparse.RequestParser()
news_parser.add_argument('title', required=True)
news_parser.add_argument('content', required=True)
news_parser.add_argument('is_private', required=True, type=bool)
news_parser.add_argument('user_id', required=True, type=int)
