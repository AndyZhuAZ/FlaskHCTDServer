from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='主页')


@app.route('/editor')
def editor():
    return render_template('editor.html')


@app.route('/editor/upload', methods=['POST'])
def upload():
    data = json.loads(request.get_data())
    filename = data['text'].strip().split('\n')[0][1:]
    print(filename)
    print(data)
    try:
        with open('static/markdown/{}/{}.md'.format(data['tip_type'], filename), 'w') as f:
            f.write(data['text'])
    except IOError:
        return '上传失败：文件 写入/读取 失败'
    else:
        return '文件上传成功'


@app.route('/getfile/<tip_type>')
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


@app.route('/tips/<tip_type>/<name>')
def tips(tip_type, name):
    with open('static/markdown/{}/{}'.format(tip_type, name), 'r') as f:
        return f.read()


@app.route('/login')
def login():
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


if __name__ == '__main__':
    app.run()
