#!/usr/bin/python3
"""defines a Flask web application with multiple routes."""

from flask import Flask, escape, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Route that displays 'Hello HBNB!'."""
    return 'Hello HBNB!'

@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Route that displays 'HBNB'."""
    return 'HBNB'

@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Route that displays 'C ' followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return 'C {}'.format(escape(text).replace('_', ' '))

@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text):
    """
    Route that displays 'Python ' followed by the value of the text variable.
    Replace underscore (_) symbols with a space.
    """
    return 'Python {}'.format(escape(text).replace('_', ' '))

@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Route that displays 'n is a number' only if n is an integer."""
    return '{} is a number'.format(n)

@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Route that displays an HTML page with an H1 tag containing 'Number: n'.
    Only if n is an integer.
    """
    return render_template('6-number_template.html', number=n)

@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
    Route that displays an HTML page with an H1 tag containing 'Number: n is even|odd'.
    Only if n is an integer.
    """
    if n % 2 == 0:
        result = 'even'
    else:
        result = 'odd'
    
    return render_template('6-number_odd_or_even.html', number=n, result=result)

if __name__ == "__main__":
    app.url_map.strict_slashes = False
    app.run(host='0.0.0.0', port=5000)
