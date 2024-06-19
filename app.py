#!/usr/bin/python3

from flask import Flask
from persistence.routes.user_routes import userRoutes  # Adjust the import

app = Flask(__name__)
app.register_blueprint(userRoutes, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)