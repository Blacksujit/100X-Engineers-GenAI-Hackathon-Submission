from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='../templates')  # Specify the path to the templates folder
    
    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app