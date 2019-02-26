from flask import Flask
from flask_mail import Mail
from flask_mongoengine import MongoEngine

import config
from views import json_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(json_api)
    return app

app = create_app()

mail = Mail(app)

mdb = MongoEngine()
mdb.init_app(app)

# 本地测试
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8888, debug=app.debug, threaded=True)