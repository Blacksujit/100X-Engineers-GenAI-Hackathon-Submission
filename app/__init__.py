from flask import Flask
from flask_caching import Cache
from flask import url_for
from flask_cors import CORS
# from PyQt5.QtWebEngineWidgets import QApplication
# from PyQt5.QtCore import QUrl
# done with the conflicts 


import os
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Specify the path to the templates and static folders
    # Set cache directory and other caching parameters
    # models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    CORS(app)
    app.secret_key = 'blackshadow'  # Replace 'your_secret_key' with a strong, unique key
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'D:\\cahc_models_folder'  # Change this to your desired cache path
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    app.config['SESSION_COOKIE_SECURE'] = False  # Use True in production
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Initialize the cache
    cache = Cache(app)
    # Set the path for the models directory (outside the app directory)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
    
    return app