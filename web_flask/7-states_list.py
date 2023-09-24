#!/usr/bin/python3
"""
This module defines a Flask web application
with a route to display a list of states.
"""

from flask import Flask, render_template
from models import storage, State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """Closes the current SQLAlchemy Session after each request."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def states_list():
    """Route that displays a list of all State objects sorted by name."""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda state: state.name)
    return render_template('7-states_list.html', states=sorted_states)


if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
