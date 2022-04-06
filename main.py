from flask import Flask, url_for, render_template, redirect, request, abort, make_response, jsonify
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/astro-project.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()




