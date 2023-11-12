import tkinter as tk
import numpy as np

# Create a Tkinter window
root = tk.Tk()
root.title("Drawing Pad")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# Initialize variables for drawing
drawing = False
coords = []

# Function to handle mouse button press (start drawing)
def start_draw(event):
    global drawing, coords
    drawing = True
    coords = []

# Function to handle mouse button release (end drawing)
def end_draw(event):
    global drawing, coords
    drawing = False
    coords.append((event.x, event.y))
    generate_grid()

# Function to handle mouse motion (drawing)
def draw(event):
    global coords
    if drawing:
        coords.append((event.x, event.y))
        canvas.create_line(coords[-2], coords[-1], width=2, fill="black")

# Bind the mouse events to their respective functions
canvas.bind("<ButtonPress-1>", start_draw)
canvas.bind("<ButtonRelease-1>", end_draw)
canvas.bind("<B1-Motion>", draw)

# Function to generate the grid within the drawn boundaries
def generate_grid():
    global coords
    if len(coords) > 1:
        x_coords, y_coords = zip(*coords)
        xmin, ymin, xmax, ymax = min(x_coords), min(y_coords), max(x_coords), max(y_coords)

        # Calculate the spacing based on your specific requirements
        spacing = 20  # Example spacing

        x_points = np.arange(xmin, xmax, spacing)
        y_points = np.arange(ymin, ymax, spacing)

        xx, yy = np.meshgrid(x_points, y_points)

        grid_points = np.column_stack((xx.flatten(), yy.flatten()))

        # Draw the grid points
        for x, y in grid_points:
            canvas.create_oval(x-1, y-1, x+1, y+1, fill="blue")

# Create a button to clear the canvas
clear_button = tk.Button(root, text="Clear Canvas", command=lambda: canvas.delete("all"))
clear_button.pack()

# Run the Tkinter main loop
root.mainloop()