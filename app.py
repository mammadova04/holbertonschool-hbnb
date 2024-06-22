#!/usr/bin/python3

from flask import Flask
from persistence.routes.user_routes import userRoutes
from persistence.routes.country_routes import countryRoutes
from persistence.routes.city_routes import cityRoutes
from persistence.routes.amenity_routes import amenityRoutes
from persistence.routes.place_routes import placeRoutes

app = Flask(__name__)
app.register_blueprint(userRoutes)
app.register_blueprint(countryRoutes)
app.register_blueprint(cityRoutes)
app.register_blueprint(amenityRoutes) 
app.register_blueprint(placeRoutes)

if __name__ == '__main__':
    app.run(debug=True)
