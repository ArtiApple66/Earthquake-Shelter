import tkinter as tk
import numpy as np
import csv

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
final_points = []
center_coords = []

def center_of_rectangle(x, y):
    """Compute the center of the rectangle given top-left coordinates."""
    return x + 20, y + 20

def save_to_csv():
    """Save the center coordinates to a specific CSV file."""
    with open('points.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["X", "Y"])  # Header
        writer.writerows(center_coords)
        print("saved")


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

    # Store the center of the rectangle
    center = center_of_rectangle(x, y)
    if center not in center_coords:
        center_coords.append(center)

canvas.bind('<Button-1>', draw)
canvas.pack()

def generate_grid():
    global coords
    if len(coords) > 1:
        x_coords, y_coords = zip(*coords)

        x_points = np.array(x_coords)
        y_points = np.array(y_coords)
        np.unique(x_points)
        np.unique(y_points)

        spacing = 40

        x_final=x_points
        y_final=y_points
        z_final = np.zeros_like(x_final)

        i = 0
        while i < len(x_final):
            final_points.append((int(x_final[i]/40), int(y_final[i]/40), int(z_final[i]/40)))
            i += 1
        print(final_points)

def clear_canvas():
    global coords, center_coords
    canvas.delete("all")
    coords = []
    center_coords = []  # Reset the center_coords as well
    for i in range(0, 400, 40):
        canvas.create_line(i, 0, i, 400, fill="lightgray")
        canvas.create_line(0, i, 400, i, fill="lightgray")

clear_button = tk.Button(root, text="Clear Canvas", command=clear_canvas)
clear_button.pack()

render_button = tk.Button(root, text="Render", command=generate_grid)
render_button.pack()

# Add a button to save the coordinates to a CSV file
save_button = tk.Button(root, text="Save to CSV", command=save_to_csv)
save_button.pack()

label = tk.Label(text="How many stories?")
label.pack()

v2 = tk.IntVar()
s2 = tk.Scale(root, variable=v2, from_=1, to=3, orient=tk.HORIZONTAL)
s2.pack()

# Run the Tkinter main loop
root.mainloop()