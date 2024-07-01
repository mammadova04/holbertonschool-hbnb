# app.py

from flask import Flask
from persistence.routes.user_routes import userRoutes
from persistence.routes.country_routes import countryRoutes
from persistence.routes.city_routes import cityRoutes
from persistence.routes.amenity_routes import amenityRoutes
from persistence.routes.place_routes import place_bp  # Update import statement
from persistence.routes.review_routes import reviewRoutes

app = Flask(__name__)
app.register_blueprint(userRoutes)
app.register_blueprint(countryRoutes)
app.register_blueprint(cityRoutes)
app.register_blueprint(amenityRoutes)
app.register_blueprint(place_bp) 
app.register_blueprint(reviewRoutes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
