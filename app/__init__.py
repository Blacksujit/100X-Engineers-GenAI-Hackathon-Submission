from flask import Flask
from flask_caching import Cache
def create_app():
    app = Flask(__name__, template_folder='../templates')  # Specify the path to the templates folder
    # Set cache directory and other caching parameters
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'F:\\100x_enginners_hackathon_genai\\app\\__pycache__'  # Change this to your desired cache path

    # Initialize the cache
    cache = Cache(app)
    
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app