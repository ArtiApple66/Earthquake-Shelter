from mayavi import mlab
import numpy as np
from woodlist import size

#parameters
length, width = map(int, size())
depth_tooth = length
length_member = length * 4
center_A4 = [0, (4 * length) + (length / 2), 0]

def plot_cuboid(center, size, color=(0, 1, 0)):
    center = np.array(center)
    size = np.array(size)
    l, w, h = size / 2

    x = center[0] + np.array([-l, -l, l, l, -l, -l, l, l])
    y = center[1] + np.array([-w, w, w, -w, -w, w, w, -w])
    z = center[2] + np.array([-h, -h, -h, -h, h, h, h, h])

    vertices = [[0, 1, 5, 4], [7, 6, 2, 3], [0, 3, 2, 1], [7, 4, 5, 6], [0, 4, 7, 3], [1, 2, 6, 5]]

    for vert in vertices:
        i0, i1, i2, i3 = vert
        xx = np.array([[x[i0], x[i1]], [x[i3], x[i2]]])
        yy = np.array([[y[i0], y[i1]], [y[i3], y[i2]]])
        zz = np.array([[z[i0], z[i1]], [z[i3], z[i2]]])
        mlab.mesh(xx, yy, zz, color=color)

def create_member(center, size, color):
    for i in range(len(center)):
        plot_cuboid(center[i], size[i], color=color)

def main(num_geometries_in_line):
    for i in range(num_geometries_in_line):
        # Adjust the x-coordinate based on the length of the building
        x_offset = i * (length_member + (space_between_members*100)) # Adjust the offset as needed

        # Create centers for A, B, and C
        centers_A = [
            [x_offset, (length / 2), 0],
            [x_offset, (length) + (length / 2), 0],
            [x_offset, (2 * length) + (length / 2), 0],
            [x_offset, (4 * length) + (length / 2), 0],
            [x_offset, center_A4[1] + length, 0],
            [x_offset, center_A4[1] + 2 * length, 0]
        ]

        centers_B = [
            [x_offset + (length / 2) + (width / 2), (center_A4[1] - length), 0],
            [x_offset - (length / 2) - (width / 2), (center_A4[1] - length), 0],
            [x_offset + (length / 2) + (width / 2), (center_A4[1] - length) - length, (length_member / 2) + (width / 2)],
            [x_offset + (length / 2) + (width / 2), (center_A4[1] - length) + length, (length_member / 2) + (width / 2)],
            [x_offset - (length / 2) - (width / 2), (center_A4[1] - length) - length, -((length_member / 2) + (width / 2))],
            [x_offset - (length / 2) - (width / 2), (center_A4[1] - length) + length, -((length_member / 2) + (width / 2))],
            [x_offset + (length / 2) + (width / 2), (center_A4[1] - length) - length, -((length_member / 2) + (width / 2))],
            [x_offset + (length / 2) + (width / 2), (center_A4[1] - length) + length, -((length_member / 2) + (width / 2))],
            [x_offset - (length / 2) - (width / 2), (center_A4[1] - length) - length, (length_member / 2) + (width / 2)],
            [x_offset - (length / 2) - (width / 2), (center_A4[1] - length) + length, (length_member / 2) + (width / 2)]
        ]

        centers_C = [
            [x_offset, (center_A4[1] - length), width],
            [x_offset, (center_A4[1] - length), -width],
            [x_offset + length, (center_A4[1] - length) + (1.5 * length + length_member / 2), width],
            [x_offset + length, (center_A4[1] - length) - (1.5 * length + length_member / 2), -width],
            [x_offset + length, (center_A4[1] - length) - (1.5 * length + length_member / 2), width],
            [x_offset + length, (center_A4[1] - length) + (1.5 * length + length_member / 2), -width],
            [x_offset - length, (center_A4[1] - length) + (1.5 * length + length_member / 2), width],
            [x_offset - length, (center_A4[1] - length) - (1.5 * length + length_member / 2), -width],
            [x_offset - length, (center_A4[1] - length) - (1.5 * length + length_member / 2), width],
            [x_offset - length, (center_A4[1] - length) + (1.5 * length + length_member / 2), -width]
        ]
        
        cuboid_long_size = [length_member, length, width]
        cuboid_short_size = [(length_member - (depth_tooth * 2)), length, width]
        
        sizes_A = [
            cuboid_long_size,
            cuboid_short_size,
            cuboid_long_size,
            cuboid_long_size,
            cuboid_short_size,
            cuboid_long_size
        ]

        sizes_B = [width, length, length_member]
        sizes_C = [length, length_member, width]

        create_member(centers_A, sizes_A, color=(0, 1, 0))
        create_member(centers_B, [sizes_B] * 10, color=(0, 0, 1))
        create_member(centers_C, [sizes_C] * 10, color=(1, 0, 0))

if __name__ == "__main__":
    
    num_geometries_in_line = int(input("Enter the number of geometries you want in a line: "))
    space_between_members = float(input("Enter the space between members (in meters): "))
    
    main(num_geometries_in_line)
    mlab.show()