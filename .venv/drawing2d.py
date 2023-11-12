import tkinter as tk
import numpy as np
from mayavi import mlab
import rhino3dm as rs
from flask import Flask
import ghhops_server as hs
import threading

# Create a Tkinter window
root = tk.Tk()
root.title("Drawing Pad")

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400, bg="white")

# Add a background grid to the canvas
for i in range(0, 400, 40):
    canvas.create_line(i, 0, i, 400, fill="lightgray")
    canvas.create_line(0, i, 400, i, fill="lightgray")

# Initialize variables for drawing
drawing = False
coords = []
pointgridfinal = []
points = []

# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)

def draw(event):
    global coords
    x = (event.x // 40) * 40
    y = (event.y // 40) * 40

    points_to_add = [(x, y), (x, y+40), (x+40, y), (x+40, y+40)]

    for point in points_to_add:
        if point not in coords:
            coords.append(point)
            canvas.create_oval(point[0]-2, point[1]-2, point[0]+2, point[1]+2, fill="blue")

    canvas.create_rectangle(x, y, x+40, y+40, outline="black")
    coords.append((x, y))

canvas.bind('<Button-1>', draw)
canvas.pack()

@hops.component(
    "/grid",
    name="pointgridfinal",
    nickname="gg",
    description="generating grid based on drawing",
    outputs=[
        hs.HopsPoint("rhino_points", "point_grid2", "Final Points", hs.HopsParamAccess.LIST),
    ]
)


def generate_grid():
    global coords, rhino_points

    if len(coords) > 1:
        # Convert the coordinates to a set to remove duplicates
        unique_coords = set(coords)

        # Convert the unique coordinates to a list
        final_coords = list(unique_coords)

        # Convert the points to a 3D space with spacing of 1
        x_final = np.array([point[0] for point in final_coords]) // 40
        y_final = np.array([point[1] for point in final_coords]) // 40
        z_final = np.zeros_like(x_final)

        rhino_points = [rs.Point3d(x, y, z) for x, y, z in zip(x_final, y_final, z_final)]

        # Plot points in 3D
        mlab.figure(bgcolor=(1, 1, 1), size=(800, 600))
        mlab.points3d(x_final, y_final, z_final, scale_factor=1, color=(0, 0, 1))

        # Display the Mayavi visualization
        mlab.show()

        return rhino_points

def clear_canvas():
    global coords
    canvas.delete("all")
    coords = []
    # Add a background grid to the canvas
    for i in range(0, 400, 40):
        canvas.create_line(i, 0, i, 400, fill="lightgray")
        canvas.create_line(0, i, 400, i, fill="lightgray")

def run_flask():
    if __name__ == "__main__":
        app.run()

# Create a button to clear the canvas
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack()

# Create a button to render
render_button = tk.Button(root, text="Render", command=generate_grid)
render_button.pack()

#run the hops component
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Run the Tkinter main loop
root.mainloop()