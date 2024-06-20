#!/usr/bin/python3

from flask import Flask
from persistence.routes.user_routes import userRoutes
from persistence.routes.country_routes import countryRoutes

app = Flask(__name__)
app.register_blueprint(userRoutes)
app.register_blueprint(countryRoutes)

if __name__ == '__main__':
    app.run(debug=True)