# app.py

from flask import Flask
from app.db.mongo import init_db
from app.controllers.public_controller import user_blueprint
from app.controllers.auth_controller import auth_controller  # Import your auth controller
from app.controllers.user_controller import user_bp  # Import your auth controller

# Initialize the Flask application
app = Flask(__name__)

# Initialize the MongoDB connection
init_db(app)

# Register the user blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_controller, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/')

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5101)
