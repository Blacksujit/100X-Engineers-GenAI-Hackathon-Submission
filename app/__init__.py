from flask import Flask
from flask_caching import Cache
# from app.gif_animation_creation import create_animated_gif
# from app.data_storytelling_video_processing import convert_gif_to_storytelling_video
# from app.deatil_infographics_creation import create_detailed_infographic
# from app.text_processing import nlp_pipeline
def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='static' )  # Specify the path to the templates folder
    # Set cache directory and other caching parameters
    app.config['CACHE_TYPE'] = 'filesystem'
    app.config['CACHE_DIR'] = 'F:\\100x_enginners_hackathon_genai\\app\\__pycache__'  # Change this to your desired cache path

    # Initialize the cache
    cache = Cache(app)
    
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
        # app.register_blueprint(create_animated_gif)
        # app.register_blueprint(convert_gif_to_storytelling_video)
        # app.register_blueprint(create_detailed_infographic)
        # app.register_blueprint(nlp_pipeline)

    return app