#!/usr/bin/python3
"""defines a Flask web application for serving Airbnb filters."""

from flask import Flask, render_template
from models import storage, State, City, Amenity

app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """Closes the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Route that displays Airbnb filters based on data from the storage engine.
    """
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    cities = sorted(storage.all(City).values(), key=lambda c: c.name)
    amenities = sorted(storage.all(Amenity).values(), key=lambda a: a.name)

    selected_states = []
    selected_cities = []
    selected_amenities = []

    return render_template('10-hbnb_filters.html',
                           states=states,
                           cities=cities,
                           amenities=amenities,
                           selected_states=selected_states,
                           selected_cities=selected_cities,
                           selected_amenities=selected_amenities)


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
