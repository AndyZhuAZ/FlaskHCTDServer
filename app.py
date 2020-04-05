from flask import Flask,render_template
import json
app = Flask(__name__)


@app.route('/')
def hello_world():
    return app.send_static_file('html/index.html')


@app.route('/editor')
def editor():
    return render_template('editor.html')

if __name__ == '__main__':
    app.run()
