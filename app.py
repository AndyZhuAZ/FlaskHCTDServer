from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os
from config import Config
from forms import LoginForm
# from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='主页')


@app.route('/editor')
@login_required
def editor():
    return render_template('editor.html')


@app.route('/editor/upload', methods=['POST'])
@login_required
def upload():
    data = json.loads(request.get_data())
    filename = data['text'].split('\n')[0][1:].strip()
    # print(filename)
    # print(data)
    try:
        with open('static/markdown/{}/{}.md'.format(data['tip_type'], filename), 'w') as f:
            f.write(data['text'])
            print('Save a file named {} in path {}'.format(filename, data['tip_type']))
    except IOError:
        return '上传失败：文件 写入/读取 失败'
    else:
        return '文件上传成功'


@app.route('/api/getfile/<tip_type>')
def get_file(tip_type):
    dic = {
        'tip_type': tip_type,
        'name': 'files',
        'num': 0,
        'filename': []
    }
    for i in os.listdir('static/markdown/{}'.format(tip_type)):
        if not i.startswith('.'):
            dic['filename'].append(i)
            dic['num'] += 1
    res = json.dumps(dic)
    return res


@app.route('/api/tips/<tip_type>/<name>')
def tips(tip_type, name):
    dic = {
        'title': name,
        'type': tip_type,
        'content': None
    }
    try:
        with open('static/markdown/{}/{}'.format(tip_type, name), 'r') as f:
            dic['content'] = f.read()
    except IOError:
        return '文件读取失败，检查文件名和路径'
    else:
        res = json.dumps(dic)
        return res


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码无效')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register')
def register():
    pass


# @app.route('/test')
# def test():
#     with open('static/markdown/心搏骤停.md') as f:
#         for line in f.readlines():
#             print(line)
#         return 'hello'
class tip():
    title = ''
    tip_type = ''
    content = ''


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    app.run()
