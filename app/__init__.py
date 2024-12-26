from flask import Flask
from flask_caching import Cache
from flask import url_for
from flask_cors import CORS
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')  # Specify the path to the templates and static folders
    # Set cache directory and other caching parameters
    CORS(app)
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'D:\\__MACOSX'  # Change this to your desired cache path

    # Initialize the cache
    cache = Cache(app)
    
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app