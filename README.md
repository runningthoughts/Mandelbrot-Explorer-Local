# Mandelbrot Explorer
This is a continuation of my exploration of Python, and here, pulling in math and plotting functions, as well as Flask, which is to conjure up and serve up the corresponding webpage locally on my machine.

## File Structure
``- Mandelbrot.py``\
``- templates/``\
``    - index.html``\
``- static/``\
``    - script.js``\
``    - styles.css``\

## Python Code
The Python code is the heart of it.  It contains both the Mandelbrot generation code, as well as the code needed to invoke Flask funcions to both configure the HTML file and host the local website, at ``http://127.0.0.1:5000/``

## HTML
The index.html is a close approximate to what you will see, and you can, to a degree, design visually, but images will not be rendered due to the template nature of the project.  In place of relative pathnames are variables that will be replaced by Flash as it renders the proper file structure:

``<img class="preset" src="{{ url_for('static', filename='p1.png') }}" onClick="preset(1)">``

This bit can be a little confusing to keep track of, but is necessary for any deployment that you might do as you are doing backend computations (in Python) that need to be hosted in order to work.

The webpage has a form with values loaded with defaults. These are what control the Mandelbrot view. Also there are 6 presets.

# JavaScript
The code extracts the data from the fields in the webpage, or alternatively injects values if the user clicks on a preset.  These values are submitted via a Form and Posted to invoke the Python funtion ``generate()``.  The JavaScript code then awaits the response, which it will inject into the space allotted for the fractal.

# CSS
Contains the styles for controlling the formatting of the various page elements.