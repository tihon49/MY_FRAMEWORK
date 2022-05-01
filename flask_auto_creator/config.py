INIT_DATA = """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config




app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

db = SQLAlchemy(app)
db.init_app(app)
db.create_all(app=app)
app.db = db

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from . import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

from .views.auth import bp as auth
from .views.main import bp as main

app.register_blueprint(auth)
app.register_blueprint(main)

"""

PROJECT_NAME = 'FLASK_PROJECT'

BASE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/bootstrap/bootstrap.css') }}"> -->
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">
    <title>FlaskApp</title>
</head>
<body>
    <div class="">
        {% block content %}
        {% endblock %}
    </div>
</body>

<script type="text/javascript" src="{{ url_for('static', filename='js/index.js') }}"></script>
</html>"""


INDEX_HTML = """{% extends 'base.html' %}

{% block content %}
    name: {{ name }}
    data: {{ data }}
{% endblock %}

"""


CONFIG_FILE = """import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'ajsdkhfioas8d7(&*()*&89sd7f98sd7f(*&DF()*&DS9f87df987'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False"""

MODELS_FILE = """from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    password = db.Column(db.String(256))"""

LOGIN_HTML = """{% extends 'base.html' %}


{% block content %}
<div class="centered">
    <div class="box-header">
        Логин
    </div>
    <div class="box">
        <div class="form">
            <form method="POST" action="/login/">
    
                <div class="box-message">
                    {% with messages = get_flashed_messages() %}
                        {% if messages %}
                            {% for message in messages %}
                                <span style="color: black">{{ message }}</span>
                            {% endfor %}
                            {% endif %}
                    {% endwith %}
                </div>
    
                <div class="field">
                    <input class="input form-control login-input" type="text" name="login" placeholder="Введите логин"
                        autofocus="" required>
                </div>
    
                <div class="field">
                    <input class="input form-control login-input" type="password" name="password"
                        placeholder="Введите пароль" required>
                </div>
                <button class="btn btn-success login-btn">Вход</button>
            </form>
        </div>
        <div class="box-footer">
            <a href="{{ url_for('auth.register') }}">Зарегистрироваться</a>
        </div>
    </div>
</div>
{% endblock %}"""

REGISTER_HTML = """{% extends 'base.html' %}

{% block content %}
<div class="centered">
    <div class="box-header">
        Регистрация
    </div>
    <div class="box">
        <div class="form">
            <form method="POST" action="/register/">
    
                <div class="box-message">
                    {% with messages = get_flashed_messages() %}
                        {% if messages %}
                            {% for message in messages %}
                                <span style="color: black">{{ message }}</span>
                            {% endfor %}
                            {% endif %}
                    {% endwith %}
                </div>
    
                <div class="field">
                    <input class="input form-control login-input" type="text" name="login" placeholder="Введите логин"
                        autofocus="" required>
                </div>
    
                <div class="field">
                    <input class="input form-control login-input" type="password" name="password" placeholder="Введите пароль" required>
                </div>
                <div class="field">
                    <input class="input form-control login-input" type="password" name="password2" placeholder="Подтвердите пароль" required>
                </div>
                <button class="btn btn-success login-btn">Зарегистрироваться</button>
            </form>
        </div>
        <div class="box-footer">
            <a href="{{ url_for('auth.login') }}">Уже зарегистрирован</a>
        </div>
    </div>
</div>
{% endblock %}"""

AUTH_PY = """from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from ..models import User
from .. import db


bp = Blueprint('auth', __name__)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(name=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('main.main'))

        flash('Не верный логин или пароль')
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user = User.query.filter_by(name=login).first()

        if user:
            flash('Такое имя уже есть.')
            return redirect(url_for('auth.login'))
        
        if not password == password2:
            flash('Пароли не совпали')
            return redirect(url_for('auth.register'))

        new_user = User(
            name=login,
            password=generate_password_hash(password, method='sha256')
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f'Создан новый пользователь: {login}')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@bp.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('main.main'))
"""

MAIN_PY = """from flask import Blueprint, render_template
from flask_login import login_required, current_user



bp = Blueprint('main', __name__)


@bp.route('/')
@login_required
def main():
    data = {
        'test': 'some test data'
    }

    return render_template(
        'index.html',
        name=current_user.name,
        data=data
    )
"""

STYLE_CSS = """body {
    background-color: rgb(255, 255, 255);
}

a {
    text-decoration: none;
    color: #5e5d5d;
}

.box {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 350px;
    height: 200px;
    text-align: center;
    border-radius: 4px;
    padding: 10px;
    box-shadow: 0 0 20px #e1e1e1;
}

.box-header {
    text-align: center;
    margin-bottom: 10px;
}

.box-footer {
    margin-top: 20px;
}

.box-message {
    max-width: 180px;
}

.centered {
    position: fixed; /* or absolute */
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.login-input, .register-input {
    margin-bottom: 5px;
    height: 20px;
}

.login-btn, .register-btn {
    width: 100%;
}"""