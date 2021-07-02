import math
import numpy as np

class CameraModel:
    def __init__(self, f, pts):
        self.r = 20
        self.phi = 0
        self.theta = 0
        self.f = f
        self.pts = np.array(pts)

    def rotate_cartesian(self, d_x, d_y):
        # we have the abolute distance of rotation
        # we "roll up" the straight line along our radius
        # r*theta = d_x, r*phi = d_y
        d_theta = math.atan2(d_y,d_x)
        abs_dist = math.sqrt(d_x*d_x + d_y*d_y)
        d_phi = math.asin(abs_dist/self.r)
        self.rotate(d_theta, d_phi)

    def shift_closer(self, d_r):
        self.r += d_r

    def zoom(self, f):
        self.f += f

    def get_outline(self):
        cart_coor = np.array(self.get_cartesian())
        centered_pts = np.subtract(self.pts, cart_coor)

        # project along v1 basis
        v1 = np.array(self.get_basis_v1())
        v1_dot = np.matmul(centered_pts, v1)

        # project along v2 basis
        v2 = np.array(self.get_basis_v2())
        v2_dot = np.matmul(centered_pts, v2)

        # project along v3 basis
        v3 = np.array(self.get_basis_v3())
        v3_dot = np.matmul(centered_pts, v3)

        transformed_pts = np.column_stack((v1_dot, v2_dot, v3_dot))
        x3_values = transformed_pts[:,2]
        real_pts = np.vstack(transformed_pts[np.argwhere(x3_values != 0)])
        real_x3 = np.vstack(x3_values[np.argwhere(x3_values != 0)])

        # (y_1, y_2) = -f*(x1, x2)/x_3
        final_matrix = -self.f*(real_pts/real_x3)

        return final_matrix[:,:2]

        #
        # return [[-self.f*x1/x3, -self.f*x2/x3] for x1, x2, x3 in centered_pts if x3 != 0]

    def print_object(self, sense):
        grid = [[" " for x in range(self.f*sense)] for i in range(self.f*sense)]
        for pt in self.get_outline():
            x1 = math.floor(pt[0]*sense + self.f*sense/2)
            x2 = math.floor(pt[1]*sense + self.f*sense/2)
            if(x1 >= len(grid) or x1 < 0 or x2 >= len(grid) or x2 < 0):
                continue
            grid[x1][x2] = "#"
        print_grid = ["".join(cols) for cols in grid]
        print_grid.insert(len(print_grid)//2, "-"*len(print_grid))
        for r in print_grid:
            print(r[:len(r)//2] + "|" + r[-len(r)//2:])

    def rotate(self, d_phi, d_theta):
        self.theta += d_theta
        self.phi += d_phi

    def get_cartesian(self):
        return [self.r*math.sin(self.phi)*math.cos(self.theta),
        self.r*math.sin(self.phi)*math.sin(self.theta),
        self.r*math.cos(self.phi)]

    def get_basis_v1(self):
        return [math.cos(self.phi)*math.cos(self.theta),
        math.cos(self.phi)*math.sin(self.theta),
        -math.sin(self.phi)]

    def get_basis_v2(self):
        v1 = self.get_basis_v1()
        v3 = self.get_basis_v3()
        return np.cross(v1, v3)

    def get_basis_v3(self):
        return [-math.sin(self.phi)*math.cos(self.theta),
        -math.sin(self.phi)*math.sin(self.theta),
        -math.cos(self.phi)]


    # move phi down
    # move theta across
    #





# convert movement on screen to degree of rotation?
# move point from part A of the screen to part B

# figure out scaling factor of the entire image
# let's do 10px = 2 for r

# figure out what theta is required to do that
# add that to the ratation
