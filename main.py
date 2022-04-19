import os
from flask import Flask, render_template, redirect, make_response, jsonify, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from data import db_session, user_resources, news_resources, space_object_resources, space_system_resources
from data.users import User
from data.news import News
from data.space_objects import SpaceObject
from data.space_systems import SpaceSystem
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm
from forms.space_system import SpaceSystemForm
from forms.space_object import SpaceObjectForm

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(user_resources.UsersListResource, '/api/users')
api.add_resource(user_resources.UsersResource, '/api/users/<int:user_id>')
api.add_resource(news_resources.NewsListResource, '/api/news')
api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')
api.add_resource(space_object_resources.SpaceObjectsListResource, '/api/space_objects')
api.add_resource(space_object_resources.SpaceObjectsResource, '/api/space_objects/<int:space_object_id>')
api.add_resource(space_system_resources.SpaceSystemsListResource, '/api/space_systems')
api.add_resource(space_system_resources.SpaceSystemsResource, '/api/space_systems/<int:space_system_id>')


def main():
    db_session.global_init("db/astro-project.db")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
@app.route("/news")
def main_page():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("main_page.html", title="AstroCat", news=news)


@app.route("/database")
def data_page():
    db_sess = db_session.create_session()
    systems = db_sess.query(SpaceSystem).all()
    return render_template("data_page.html", title="База данных", systems=systems)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            username=form.username.data,
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter((User.email == form.login.data) | (User.username == form.login.data)).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление записи',
                           form=form)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование записи',
                           form=form
                           )


@app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_news(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/add_system', methods=['GET', 'POST'])
@login_required
def add_system():
    form = SpaceSystemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        system = SpaceSystem()
        system.name = form.name.data
        system.galaxy = form.galaxy.data
        system.about = form.about.data
        current_user.space_systems.append(system)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/database')
    return render_template('space_system.html', title='Добавление космической системы',
                           form=form)


@app.route('/edit_system/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_system(id):
    form = SpaceSystemForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == id).first()
        if system:
            form.name.data = system.name
            form.galaxy.data = system.galaxy
            form.about.data = system.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == id).first()
        if system:
            system.name = form.name.data
            system.galaxy = form.galaxy.data
            system.about = form.about.data
            db_sess.commit()
            return redirect('/database')
        else:
            abort(404)
    return render_template('space_system.html',
                           title='Редактирование космической системы',
                           form=form
                           )


@app.route('/add_space_object/<int:id>', methods=['GET', 'POST'])
@login_required
def add_space_object(id):
    form = SpaceObjectForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        space_object = SpaceObject()
        space_object.name = form.name.data
        space_object.space_type = form.space_type.data
        space_object.radius = form.radius.data
        space_object.period = form.period.data
        space_object.ex = form.ex.data
        space_object.v = form.v.data
        space_object.p = form.p.data
        space_object.g = form.g.data
        space_object.m = form.m.data
        space_object.sputnik = form.sputnik.data
        space_object.atmosphere = form.atmosphere.data
        space_object.about = form.about.data
        space_object.system = id
        current_user.space_objects.append(space_object)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/database')
    return render_template('space_object.html', title='Добавление космического объекта',
                           form=form)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
