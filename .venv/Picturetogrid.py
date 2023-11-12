import numpy as np
from PIL import Image

# Load the image (for PDF, you would convert it to an image first)
image_path = "square_noun_002_35417.jpg"  # Replace with the path to your image
image = Image.open(image_path)

# Get the dimensions of the image
width, height = image.size

# Determine the minimum and maximum coordinates
xmin, ymin, xmax, ymax = 0, 0, width, height

# Calculate the spacing based on your specific requirements
spacing = 20  # Example spacing

x_points = np.arange(xmin, xmax, spacing)
y_points = np.arange(ymin, ymax, spacing)

xx, yy = np.meshgrid(x_points, y_points)

grid_points = np.column_stack((xx.flatten(), yy.flatten()))

import matplotlib.pyplot as plt

# Unpack the coordinates
x, y = zip(*grid_points)

# Create a scatter plot
plt.scatter(x, y, c='blue', marker='.')

# Optionally, add additional elements to the plot
# For example, if you have lines from the PDF or drawing, you can add them as well.

# Show the plot
plt.show()
