import os

from flask import Flask, render_template, request
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('html/index.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')


@app.route('/editor/upload', methods=['POST'])
def upload():
    data = json.loads(request.get_data())
    filename = data['text'].strip().split('\n')[0][1:]
    print(filename)
    with open('static/markdown/{}.md'.format(filename), 'w') as f:
        f.write(data['text'])
    return 'succeed'


@app.route('/getfile')
def get_file():
    dic = {
        'name': 'files',
        'num': 0,
        'filename': []
    }
    for i in os.listdir('static/markdown'):
        if not i.startswith('.'):
            dic['filename'].append(i)
            dic['num'] += 1
    res = json.dumps(dic)
    return res


@app.route('/tips/<tip_type>/<name>')
def tips(tip_type,name):
    with open('static/markdown/{}/{}'.format(tip_type,name), 'r') as f:
        return f.read()


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

if __name__ == '__main__':
    app.run()
