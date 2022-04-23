from flask_restful import Resource, abort
from flask import jsonify
from data import db_session
from data.news import News
from data.parsers import news_parser


class NewsResource(Resource):

    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user.name', 'is_private', 'photo_path'))})

    def post(self, news_id):
        abort_if_news_not_found(news_id)
        args = news_parser.parse_args()
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        news.title = args['title']
        news.content = args['content']
        news.is_private = args['is_private']
        news.user_id = args['user_id']
        session.commit()
        return jsonify({'success': 'OK'})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class NewsListResource(Resource):

    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name', 'photo_path')) for item in news]})

    def post(self):
        args = news_parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")
