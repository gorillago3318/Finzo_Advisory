from flask import Flask
from backend.extensions import db, migrate
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///refinance_chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_default_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from backend.routes.chatbot import chatbot_bp
    from backend.routes.auth import auth_bp
    from backend.routes.admin import admin_bp
    from backend.routes.agent import agent_bp

    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(agent_bp, url_prefix='/api/agent')

    with app.app_context():
        from backend import models  # Import models for Flask-Migrate

    return app

# Expose the app object for command-line commands
app = create_app()

if __name__ == "__main__":
    app.run()
