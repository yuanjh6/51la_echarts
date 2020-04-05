from flask import Flask

from app.api import app_api

app = Flask("my_flask", static_folder="static", template_folder="templates")
app.register_blueprint(app_api, url_prefix='/api')


@app.route('/', methods=['get'])
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=False, processes=True)
    print('main End')
