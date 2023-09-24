#!/usr/bin/python3
"""
This module defines a Flask web application
with a route to display cities by state.
"""

from flask import Flask, render_template
from models import storage, State, City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """Closes the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Route that displays a list of states and cities."""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    cities_by_state = {}
    for state in sorted_states:
        if storage.__class__.__name__ == 'DBStorage':
            cities = state.cities
        else:
            cities = state.cities
        sorted_cities = sorted(cities, key=lambda city: city.name)
        cities_by_state[state] = sorted_cities

    return render_template('8-cities_by_states.html', cities_by_state=cities_by_state)


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
