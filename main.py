import os
from flask import Flask, render_template, redirect, make_response, jsonify, abort, request, url_for, send_file
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

app = Flask(__name__)  # создаём приложение Flask
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'  # секретный ключ
app.config['NEWS_PHOTO_FOLDER'] = 'img/news_photos/'  # путь к ресурсам записей
login_manager = LoginManager()  # для авторизации
login_manager.init_app(app)  # инициализация в приложении
api = Api(app)  # создание api-ресурса
"""Добавление ресурсов всех моделей со ссылками"""
api.add_resource(user_resources.UsersListResource, '/api/users')
api.add_resource(user_resources.UsersResource, '/api/users/<int:user_id>')
api.add_resource(news_resources.NewsListResource, '/api/news')
api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')
api.add_resource(space_object_resources.SpaceObjectsListResource, '/api/space_objects')
api.add_resource(space_object_resources.SpaceObjectsResource, '/api/space_objects/<int:space_object_id>')
api.add_resource(space_system_resources.SpaceSystemsListResource, '/api/space_systems')
api.add_resource(space_system_resources.SpaceSystemsResource, '/api/space_systems/<int:space_system_id>')
avatars = Avatars(app)  # для удобной работы с аватарками


def main():
    """Запуск приложения"""
    db_session.global_init("db/astro-project.db")  # объявление базы данных
    port = int(os.environ.get("PORT", 8080))  # порт
    app.run(host='0.0.0.0', port=port)  # запуск


@login_manager.user_loader
def load_user(user_id):
    """Загрузка текущего пользователя"""
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    """Выход пользователя"""
    logout_user()
    return redirect("/")  # перевод на главную страницу


@app.route("/", methods=['GET', 'POST'])
@app.route("/news", methods=['GET', 'POST'])
def main_page():
    """Главная страница"""
    db_sess = db_session.create_session()
    if current_user.is_authenticated:  # если авторизован
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))  # все свои записи
    else:
        news = db_sess.query(News).filter(News.is_private != True)  # только публичные
    return render_template("main_page.html", title="AstroCat", news=news, avatars=avatars)  # отображение html-файла


@app.route("/database", methods=['GET', 'POST'])
def data_page():
    """Страница с Базой Данных"""
    db_sess = db_session.create_session()
    solar_system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == 1).first()  # специально для Солнечной системы
    systems = db_sess.query(SpaceSystem).filter(SpaceSystem.id != 1)  # все остальные
    return render_template("data_page.html", title="AstroCat", systems=systems, solar_system=solar_system)


@app.route('/space_object/<name>', methods=['GET', 'POST'])
def space_object_info(name):
    """Страница с информацией о космическом объекте"""
    db_sess = db_session.create_session()
    space_object = db_sess.query(SpaceObject).filter(SpaceObject.name == name).first()  # поиск по имени
    if space_object:
        return render_template('space_object_info.html', title=space_object.name, space_object=space_object)
    return make_response(jsonify({'error': 'Not found'}), 404)  # если не найден


@app.route('/user/<username>', methods=['GET', 'POST'])
def user_profile(username):
    """Страница с профилем пользователя"""
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()  # поиск по логину
    if user:
        return render_template('user_profile.html', title='Профиль', user=user, news=user.news)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """Страница с формой регистрации"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data.strip() != form.password_again.data.strip():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают!")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data.strip()).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть!")
        if db_sess.query(User).filter(User.username == form.username.data.strip()).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Логин занят!")
        user = User(
            username=form.username.data.strip(),
            name=form.name.data.strip(),
            surname=form.surname.data.strip(),
            email=form.email.data.strip(),
            age=form.age.data,
            about=form.about.data.strip()
        )  # создание пользователя
        user.set_password(form.password.data.strip())  # хэширование пароля
        db_sess.add(user)  # добавление пользователя
        db_sess.commit()  # подтверждение изменений
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница с формой авторизации пользователя"""
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            (User.email == form.login.data.strip()) | (User.username == form.login.data.strip())).first()
        if user and user.check_password(form.password.data.strip()):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news',  methods=['GET', 'POST'])
@login_required
def add_news():
    """Страница с формой добавления записи"""
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data.strip()
        news.content = form.content.data.strip()
        news.is_private = form.is_private.data
        file = form.photo.data  # загрузка файла (изображения)
        if file:
            filename = secure_filename(file.filename)
            news.photo_path = url_for('static', filename=app.config['NEWS_PHOTO_FOLDER'] + filename)
            file.save(f'static/img/news_photos/{filename}')  # сохранение файла
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect(f'/user/{news.user.username}')
    return render_template('news.html', title='AstroCat',
                           form=form)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    """Страница с формой редактирования записи"""
    form = NewsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title.strip()
            form.content.data = news.content.strip()
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data.strip()
            news.content = form.content.data.strip()
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
    """Удаление записи"""
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        user = news.user
        db_sess.delete(news)  # удаление
        db_sess.commit()
        return redirect(f'/user/{user.username}')
    else:
        abort(404)


@app.route('/add_system', methods=['GET', 'POST'])
@login_required
def add_system():
    """Страница с формой добавления звёздной системы"""
    form = SpaceSystemForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(SpaceSystem).filter(SpaceSystem.name == form.name.data.strip()).first():
            return render_template('space_system.html', title='AstroCat',
                                   form=form,
                                   message="Такая система уже есть!")
        system = SpaceSystem()
        system.name = form.name.data.strip()
        system.galaxy = form.galaxy.data.strip()
        system.about = form.about.data.strip()
        current_user.space_systems.append(system)
        db_sess.merge(current_user)
        db_sess.commit()
        os.mkdir(f'static/img/{system.name}')  # создание папки для изображения космических объектов системы
        return redirect('/database')
    return render_template('space_system.html', title='AstroCat',
                           form=form)


@app.route('/edit_system/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_system(id):
    """Страница с формой редактирования звёздной системы"""
    form = SpaceSystemForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == id).first()
        if system:
            form.name.data = system.name.strip()
            form.galaxy.data = system.galaxy.strip()
            form.about.data = system.about.strip()
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == id).first()
        if system:
            new_system = db_sess.query(SpaceSystem).filter(SpaceSystem.name == form.name.data.strip()).first()
            if new_system and new_system != new_system:
                return render_template('space_system.html', title='AstroCat',
                                       form=form,
                                       message="Такая система уже есть!")
            os.rename(f'static/img/{system.name}', f'static/img/{form.name.data}')  # переименовываем папку
            system.name = form.name.data.strip()
            system.galaxy = form.galaxy.data.strip()
            system.about = form.about.data.strip()
            db_sess.commit()
            return redirect('/database')
        else:
            abort(404)
    return render_template('space_system.html',
                           title='AstroCat',
                           form=form
                           )


@app.route('/delete_system/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_system(id):
    """Удаление звёздной системы"""
    db_sess = db_session.create_session()
    system = db_sess.query(SpaceSystem).filter(SpaceSystem.id == id,
                                               (SpaceSystem.user == current_user) | (current_user.id == 1)
                                               ).first()
    if system:
        db_sess.delete(system)
        db_sess.commit()
        return redirect('/database')
    else:
        abort(404)


@app.route('/add_space_object/<int:id>', methods=['GET', 'POST'])
@login_required
def add_space_object(id):
    """Страница с формой добавления космического объекта"""
    form = SpaceObjectForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(SpaceObject).filter(SpaceObject.name == form.name.data).first():
            return render_template('space_object.html', title='AstroCat',
                                   form=form,
                                   message="Такой объект уже есть!")
        space_object = SpaceObject()
        space_object.name = form.name.data.strip()
        space_object.space_type = form.space_type.data.strip()
        space_object.radius = form.radius.data
        space_object.period = form.period.data
        space_object.ex = form.ex.data
        space_object.v = form.v.data
        space_object.p = form.p.data
        space_object.g = form.g.data
        space_object.m = form.m.data
        space_object.sputnik = form.sputnik.data
        space_object.atmosphere = form.atmosphere.data.strip()
        space_object.about = form.about.data.strip()
        space_object.system = id
        current_user.space_objects.append(space_object)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/database')
    return render_template('space_object.html', title='AstroCat',
                           form=form)


@app.route('/edit_space_object/<name>', methods=['GET', 'POST'])
@login_required
def edit_space_object(name):
    """Страница с формой редактирования космического объекта """
    form = SpaceObjectForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        space_object = db_sess.query(SpaceObject).filter(SpaceObject.name == name).first()
        if space_object:
            form.name.data = space_object.name.strip()
            form.space_type.data = space_object.space_type.strip()
            form.radius.data = space_object.radius
            form.period.data = space_object.period
            form.ex.data = space_object.ex
            form.v.data = space_object.v
            form.p.data = space_object.p
            form.g.data = space_object.g
            form.m.data = space_object.m
            form.sputnik.data = space_object.sputnik
            form.atmosphere.data = space_object.atmosphere.strip()
            form.about.data = space_object.about.strip()
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        space_object = db_sess.query(SpaceObject).filter(SpaceObject.name == name).first()
        if space_object:
            new_space_object = db_sess.query(SpaceObject).filter(SpaceObject.name == form.name.data.strip()).first()
            if new_space_object and new_space_object != space_object:
                return render_template('space_object.html', title='AstroCat',
                                       form=form,
                                       message="Такой объект уже есть!")
            space_object.name = form.name.data.strip()
            space_object.space_type = form.space_type.data.strip()
            space_object.radius = form.radius.data
            space_object.period = form.period.data
            space_object.ex = form.ex.data
            space_object.v = form.v.data
            space_object.p = form.p.data
            space_object.g = form.g.data
            space_object.m = form.m.data
            space_object.sputnik = form.sputnik.data
            space_object.atmosphere = form.atmosphere.data.strip()
            space_object.about = form.about.data.strip()
            file = form.image.data
            if file:
                filename = secure_filename(file.filename)
                if space_object.space_system.id == 1:
                    space_object.image_path = url_for('static',
                                                      filename='img/solar_img/' + filename)
                    file.save(f'static/img/solar_img/{filename}')
                else:
                    space_object.image_path = url_for('static',
                                                      filename=f'img/{space_object.space_system.name}' + filename)
                    file.save(f'static/img/{space_object.space_system.name}/{filename}')
            db_sess.commit()
            return redirect(f'/space_object/{space_object.name}')
        else:
            abort(404)
    return render_template('space_object.html',
                           title='AstroCat',
                           form=form, image=space_object.image_path
                           )


@app.route('/delete_space_object/<name>', methods=['GET', 'POST'])
@login_required
def delete_space_object(name):
    """Удаление космического объекта"""
    db_sess = db_session.create_session()
    space_object = db_sess.query(SpaceObject).filter(SpaceObject.name == name,
                                               (SpaceObject.user == current_user) | (current_user.id == 1)
                                               ).first()
    if space_object:
        db_sess.delete(space_object)
        db_sess.commit()
        return redirect('/database')
    else:
        abort(404)


@app.route('/edit_user/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    """Страница с формой редактирования пользователя"""
    form = EditUserForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        if user:
            form.username.data = user.username.strip()
            form.name.data = user.name.strip()
            form.surname.data = user.surname.strip()
            form.age.data = user.age
            form.about.data = user.about.strip()
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username).first()
        if user:
            new_user = db_sess.query(User).filter(User.username == form.username.data.strip()).first()
            if new_user and new_user != user:
                return render_template('user.html', title='AstroCat',
                                       form=form,
                                       message="Логин занят!")
            user.username = form.username.data.strip()
            user.name = form.name.data.strip()
            user.surname = form.surname.data.strip()
            user.age = form.age.data
            user.about = form.about.data.strip()
            db_sess.commit()
            return redirect(f'/user/{user.username}')
        else:
            abort(404)
    return render_template('user.html',
                           title='AstroCat',
                           form=form
                           )


@app.route('/download_file')
def download_file():
    """Загрузка файла (модели Солнечной системы)"""
    return send_file('app/dist/modelSolarSystem.exe')


@app.errorhandler(404)
def not_found(error):
    """Обработка ошибки 404"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    main()  # запуск приложения
