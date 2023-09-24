#!/usr/bin/python3
"""
This module defines a Flask web application
with routes to display states and their cities.
"""

from flask import Flask, render_template
from models import storage, State, City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """Closes the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Route that displays a list of all State objects."""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('9-states.html', states=sorted_states)


@app.route('/states/<id>', strict_slashes=False)
def states_cities(id):
    """Route that displays a list of cities for a specific State."""
    state = storage.get(State, id)
    if state is not None:
        cities = sorted(state.cities, key=lambda city: city.name)
        return render_template('9-states_cities.html', state=state, cities=cities)
    else:
        return render_template('9-not_found.html')


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
