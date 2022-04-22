import os
from flask import Flask, render_template, redirect, make_response, jsonify, abort, request, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_restful import Api
from flask_avatars import Avatars
from werkzeug.utils import secure_filename

from data import db_session, user_resources, news_resources, space_object_resources, space_system_resources
from data.users import User
from data.news import News
from data.space_objects import SpaceObject
from data.space_systems import SpaceSystem
from forms.news import NewsForm
from forms.user import RegisterForm, LoginForm, EditUserForm
from forms.space_system import SpaceSystemForm
from forms.space_object import SpaceObjectForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['NEWS_PHOTO_FOLDER'] = 'img/news_photos/'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)
api.add_resource(user_resources.UsersListResource, '/api/users')
api.add_resource(user_resources.UsersResource, '/api/users/<int:user_id>')
api.add_resource(news_resources.NewsListResource, '/api/news')
api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')
api.add_resource(space_object_resources.SpaceObjectsListResource, '/api/space_objects')
api.add_resource(space_object_resources.SpaceObjectsResource, '/api/space_objects/<int:space_object_id>')
api.add_resource(space_system_resources.SpaceSystemsListResource, '/api/space_systems')
api.add_resource(space_system_resources.SpaceSystemsResource, '/api/space_systems/<int:space_system_id>')
avatars = Avatars(app)


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


@app.route("/", methods=['GET', 'POST'])
@app.route("/news", methods=['GET', 'POST'])
def main_page():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("main_page.html", title="AstroCat", news=news, avatars=avatars)


@app.route("/database", methods=['GET', 'POST'])
def data_page():
    db_sess = db_session.create_session()
    systems = db_sess.query(SpaceSystem).all()
    return render_template("data_page.html", title="AstroCat", systems=systems)


@app.route('/space_object/<int:id>', methods=['GET', 'POST'])
def space_object_info(id):
    db_sess = db_session.create_session()
    space_object = db_sess.query(SpaceObject).filter(SpaceSystem.id == id).first()
    if space_object:
        return render_template('space_object_info.html', title=space_object.name, space_object=space_object)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    if user:
        return render_template('user_profile.html', title='Профиль', user=user, news=user.news)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Логин занят!")
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
        file = form.photo.data
        if file:
            filename = secure_filename(file.filename)
            news.photo_path = url_for('static', filename=app.config['NEWS_PHOTO_FOLDER'] + filename)
            file.save(f'static/img/news_photos/{filename}')
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/user/{news.user.username}')
    return render_template('news.html', title='AstroCat',
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
            file = form.photo.data
            if file:
                filename = secure_filename(file.filename)
                news.photo_path = url_for('static', filename=app.config['NEWS_PHOTO_FOLDER'] + filename)
                file.save(f'static/img/news_photos/{filename}')
            db_sess.commit()
            return redirect(f'/user/{news.user.username}')
        else:
            abort(404)
    return render_template('news.html',
                           title='AstroCat',
                           form=form, photo=news.photo_path
                           )


@app.route('/delete_news/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_news(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        user = news.user
        db_sess.delete(news)
        db_sess.commit()
        return redirect(f'/user/{user.username}')
    else:
        abort(404)


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
    return render_template('space_system.html', title='AstroCat',
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
                           title='AstroCat',
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
    return render_template('space_object.html', title='AstroCat',
                           form=form)


@app.route('/edit_space_object/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_space_object(id):
    form = SpaceObjectForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        space_object = db_sess.query(SpaceObject).filter(SpaceObject.id == id).first()
        if space_object:
            form.name.data = space_object.name
            form.space_type.data = space_object.space_type
            form.radius.data = space_object.radius
            form.period.data = space_object.period
            form.ex.data = space_object.ex
            form.v.data = space_object.v
            form.p.data = space_object.p
            form.g.data = space_object.g
            form.m.data = space_object.m
            form.sputnik.data = space_object.sputnik
            form.atmosphere.data = space_object.atmosphere
            form.about.data = space_object.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        space_object = db_sess.query(SpaceObject).filter(SpaceObject.id == id).first()
        if space_object:
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
            db_sess.commit()
            return redirect(f'/space_object/{id}')
        else:
            abort(404)
    return render_template('space_object.html',
                           title='AstroCat',
                           form=form
                           )

@app.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    form = EditUserForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        if user:
            form.username.data = user.username
            form.name.data = user.name
            form.surname.data = user.surname
            form.age.data = user.age
            form.about.data = user.about
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        if user:
            new_user = db_sess.query(User).filter(User.username == form.username.data).first()
            if new_user and new_user != user:
                return render_template('user.html', title='AstroCat',
                                       form=form,
                                       message="Логин занят!")
            user.username = form.username.data
            user.name = form.name.data
            user.surname = form.surname.data
            user.age = form.age.data
            user.about = form.about.data
            db_sess.commit()
            return redirect(f'/user/{user.username}')
        else:
            abort(404)
    return render_template('user.html',
                           title='AstroCat',
                           form=form
                           )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()
