
import tkinter as tk
import numpy as np
from mayavi import mlab
from flask import Flask
import ghhops_server as hs
import threading
import rhino3dm as rs

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
pointgridfinalb = []
lines = []

# register hops app as middleware
app = Flask(__name__)
hops = hs.Hops(app)

#draw the rectangels
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
    coords.append((x,y))

canvas.bind('<Button-1>', draw)
canvas.pack()

@hops.component(
    "/grid",
    name="pointgridfinal",
    nickname="gg",
    description="generating grid based on drawing",
    outputs=[
        hs.HopsPoint("pointgridfinal", "point_grid", "Final Points", hs.HopsParamAccess.LIST),
    ]
)

# Function to generate the grid within the drawn boundaries
def generate_grid():   
    global coords, v2
    if len(coords) > 1:
        x_coords, y_coords = zip(*coords)

        x_points = np.array(x_coords)
        y_points = np.array(y_coords)
        np.unique(x_points)
        np.unique(y_points)
        length = len(x_points)

        # Set spacing to 1 for grid points
        spacing = 40

        # Ensure z-spacing matches y-spacing
        z_spacing = spacing

        z_points = np.arange(0, v2.get() * 3 * z_spacing, z_spacing)
        z_coords = []

        i = 0
        while i < len(z_points):
            z_coords.extend(list(zip(np.full(length, z_points[i]), x_points, y_points)))
            i += 1

        # Extract x, y, z coordinates
        z_final, x_final, y_final = zip(*z_coords)

        mlab.clf()

        # Create a 3D scatter plot with Mayavi
        mlab.points3d(x_final, y_final, z_final, color=(0, 0, 1), scale_factor=10)

        #get the coordinates of the points in a list
        i = 0
        while i < len(x_final):
            pt = rs.Point3d(int(x_final[i]/40), int(y_final[i]/40), int(z_final[i]/40))
            pointgridfinal.append(pt)
            i += 1

        print(pointgridfinal)
        return pointgridfinal

def run_flask():
    if __name__ == "__main__":
        app.run()

def clear_canvas():
    global coords
    canvas.delete("all")
    coords = []

    # Add a background grid to the canvas
    for i in range(0, 400, 40):
        canvas.create_line(i, 0, i, 400, fill="lightgray")
        canvas.create_line(0, i, 400, i, fill="lightgray")

    #empty the mayavi viewer
    mlab.clf()

# Create a button to clear the canvas
clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack()

# Create a button to render
render_button = tk.Button(root, text="Render", command=generate_grid)
render_button.pack()

label = tk.Label(text="How many stories?")
label.pack()

v2 = tk.IntVar()
s2 = tk.Scale( root, variable = v2, from_ = 1, to = 3, orient = tk.HORIZONTAL)
s2.pack()  

#run the hops component
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Run the Tkinter main loop
root.mainloop() 
