import tkinter as tk
import ../models/camera_model
import math
import matplotlib.pyplot as plt
import numpy as np


class GUI:
    def __init__(self):
        self.w = tk.Tk()
        self.c = tk.Canvas(self.w, width=500, height=500)
        self.c.pack()

    def put_pts(self, pts, pt_size):
        for pt in pts:
            python_green = "#476042"
            (x1, y1) = (pt[0] - pt_size/2, pt[1] - pt_size/2)
            (x2, y2) = (x1 + pt_size/2, y1 + pt_size/2)
            self.c.create_oval(x1, y1, x2, y2, fill=python_green)


def make_square(x1, x2):
    square_pts = []

    for x in range(x1, x2):
        # horizontal lines
        square_pts.append((x, 0))
        square_pts.append((x, x2))

        # vertical lines
        square_pts.append((0, x))
        square_pts.append((x2, x))

    return square_pts

def make_cube(size, density):
    cube_pts = []
    for i in range(size*density):
        for j in range(size*density):
            for k in range(size*density):
                cube_pts.append([i/density, j/density, k/density])
    return cube_pts

def make_plane(size, density):
    plane_pts = []
    for i in range(size*density):
        for j in range(size*density):
            plane_pts.append([i/density, j/density, 0])
    return plane_pts


def make_tri_prism(size, density):
    tri_pts = []
    for z_density in range(size*density):
        for x_density in range(size*density):
            # go down left
            # y = -x + size/2
            tri_pts.append([x_density/density, -x_density/density+size/2, z_density/density])
            # y = x + size/2
            tri_pts.append([-x_density/density, -x_density/density+size/2, z_density/density])
            # y = -size/2
            tri_pts.append([-x_density/density, -size/2, z_density/density])
            tri_pts.append([x_density/density, -size/2, z_density/density])
    return tri_pts

# frame = GUI()
pts = make_tri_prism(5, 10)
c_model = camera_model.CameraModel(2, pts)
plt.axis([-.5,.5,-.5,.5])
for i in range(int(2*360)):
    c_model.rotate(math.pi/360, 0)
    perspective = c_model.get_outline()
    plt.axis([-.5,.5,-.5,.5])
    plt.scatter(perspective[:,0], perspective[:, 1])
    plt.savefig('images/' + str(i) + '.png')
    plt.close()

# get points, put them in



# print("90")
# c_model.rotate_cartesian(0, 10)
# c_model.print_object(20)
# print("180")
# c_model.rotate_cartesian(0, 10)
# c_model.print_object(20)
# print("270")
# c_model.rotate_cartesian(0, 10)
# c_model.print_object(20)
# print("360")
# c_model.rotate_cartesian(0, 10)
# c_model.print_object(20)
