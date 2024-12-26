from flask import Flask
from flask_caching import Cache
from flask import url_for
from flask_cors import CORS
<<<<<<< HEAD
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Specify the path to the templates and static folders
    # Set cache directory and other caching parameters
    CORS(app)
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'D:\\__MACOSX'  # Change this to your desired cache path

    # Initialize the cache
    cache = Cache(app)
    
=======
import os
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Specify the path to the templates and static folders
    # Set cache directory and other caching parameters
    # models_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    CORS(app)
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'F:\\cache_folder'  # Change this to your desired cache path
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300
    # Initialize the cache
    cache = Cache(app)
    # Set the path for the models directory (outside the app directory)

>>>>>>> 795a1e6 ( Errors are there in csv to video moddule will do tommorow ✅)
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app