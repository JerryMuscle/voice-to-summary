from flask import Flask

from flask import Flask

def create_app():
    """Flaskアプリケーションを初期化する関数"""
    app = Flask(__name__)

    return app