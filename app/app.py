# from flask import Flask
# from app.db import init_db  # Import the init_db function
# from app.routes import create_routes  # Import the function to create routes

# app = Flask(__name__)

# # Initialize the database
# init_db(app)

# # Create routes
# create_routes(app)  # Call create_routes with only the app argument

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# app/app.py

# app/app.py

from flask import Flask
from app.db.mongo import init_db
from app.controllers.public_controller import user_blueprint
from app.controllers.auth_controller import auth_controller  # Import your auth controller
from app.controllers.user_controller import user_bp  # Import your auth controller

app = Flask(__name__)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(auth_controller, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5101)
