from flask_restful import reqparse

user_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов пользователя
user_parser.add_argument('username', required=True)
user_parser.add_argument('surname', required=True)
user_parser.add_argument('name', required=True)
user_parser.add_argument('age', type=int)
user_parser.add_argument('about')
user_parser.add_argument('email', required=True)
user_parser.add_argument('password', required=True)


news_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов записи
news_parser.add_argument('title', required=True)
news_parser.add_argument('content', required=True)
news_parser.add_argument('is_private', required=True, type=bool)
news_parser.add_argument('user_id', required=True, type=int)

space_object_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов космического объекта
space_object_parser.add_argument('name', required=True)
space_object_parser.add_argument('space_type')
space_object_parser.add_argument('radius', type=int)
space_object_parser.add_argument('period', type=int)
space_object_parser.add_argument('ex', type=int)
space_object_parser.add_argument('v', type=int)
space_object_parser.add_argument('p', type=int)
space_object_parser.add_argument('g', type=int)
space_object_parser.add_argument('m', type=int)
space_object_parser.add_argument('sputnik', type=int)
space_object_parser.add_argument('atmosphere')
space_object_parser.add_argument('about')
space_object_parser.add_argument('creator', required=True, type=int)

space_system_parser = reqparse.RequestParser()  # парсер аргументов для ресурсов космической системы
space_system_parser.add_argument('name', required=True)
space_system_parser.add_argument('galaxy')
space_system_parser.add_argument('about')
space_system_parser.add_argument('creator', required=True, type=int)
