from flask import Flask
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('html/index.html')


@app.route('/editor')
def editor():
    return app.send_static_file('html/editor.html')

if __name__ == '__main__':
    app.run()
