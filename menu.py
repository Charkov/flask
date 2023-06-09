import os

from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.user import RegisterForm
from forms.LoginForm import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/main_menu')
def menu():
    db_sess = db_session.create_session()
    attractions = {'d1': 'Успенский собор', 'd2': 'парк имени 30-летия Победы'}
    return render_template("main menu.html", attractions=attractions)


@app.route('/d1/<name_page>')
def perv(name_page):
    return render_template("страница1.html", name=name_page)


@app.route('/d2/<name_page>')
def vtor(name_page):
    return render_template("страница2.html", name=name_page)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="There is already such a user")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
#    app.run(port=8000, host='127.0.0.1')
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
