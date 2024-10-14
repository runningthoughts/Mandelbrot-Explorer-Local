import sys
import os 
import signal

# Handles in-memory image handling instead of writing to a file
from io import BytesIO

# Flask creates the webserver to serve up the images
from flask import Flask, render_template, request, send_file
from flask_cors import CORS

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlibz

# Allows Ctrl-C to work in PC environment
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# Create the server and enable CORS
app = Flask(__name__)
CORS(app)

#################################################################
# Calculate the Mandelbrot set
# xmin-ymax variables define the range of the complex plane
# img variables allow mapping to an image
# Max iterations controls a sort of resolution of the final image
#################################################################
def mandelbrot_set(xmin, xmax, ymin, ymax, img_width, img_height, max_iter):
    real = np.linspace(xmin, xmax, img_width)
    imag = np.linspace(ymin, ymax, img_height)
    real, imag = np.meshgrid(real, imag)
    c = real + 1j * imag
    z = np.zeros_like(c)
    mandelbrot = np.full(c.shape, max_iter, dtype=int)

    mask = np.full(c.shape, True, dtype=bool)
    for i in range(max_iter):
        z[mask] = z[mask] ** 2 + c[mask]
        mask_new = (np.abs(z) <= 2)
        mandelbrot[mask & (~mask_new)] = i
        mask = mask & mask_new
        if not mask.any():
            break

    return mandelbrot

# Serve up the main index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Generate the Mandelbrot when the user clicks on Generate
# (which causes a Form Submission using the POST method.
@app.route('/generate', methods=['POST'])

#################################################################
# Extract the Form data, then generates the Mandelbrot using the
# function above, then uses Matplotlib to plot it out, using the
# viridis colormap initially (user can change this in the webpage
#################################################################
def generate():
    print("Generate called")
    # Get parameters from the form data
    center_x = float(request.form.get('center_x', '-0.5'))
    center_y = float(request.form.get('center_y', '0.0'))
    zoom = float(request.form.get('zoom', '1.0'))
    max_iter = int(request.form.get('max_iter', '200'))
    color_map = request.form.get('color_map', 'viridis')

    img_width, img_height = 1200, 1200
    zoom_factor = 1 / zoom
    xmin = center_x - zoom_factor
    xmax = center_x + zoom_factor
    ymin = center_y - zoom_factor
    ymax = center_y + zoom_factor

    # Generate the fractal image
    mandelbrot_image = mandelbrot_set(
        xmin, xmax, ymin, ymax, img_width, img_height, max_iter
    )

    # Plot the fractal
    plt.figure(figsize=(6, 6), dpi=220)
    plt.imshow(
        mandelbrot_image,
        extent=(xmin, xmax, ymin, ymax),
        cmap=color_map,
        interpolation='bilinear'
    )
    plt.axis('off')

    # Save the plot to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)

    return send_file(buf, mimetype='image/png')

# AWS Lambda handler
    # def lambda_handler(event, context):
    # from awslambdaric import lambda_handler as serverless_wsgi_handler
    # return serverless_wsgi_handler(app, event, context)

if __name__ == '__main__':
    app.run(debug=True)
