import numpy as np
import random

class RandomFilter:

    def pass_filter(self):
        return random.randint(1, 100) != 1

class FlatToThree:
    def __init__(self, f, z, l, w, n):

        self.f = f
        self.z = z
        self.x = l/2
        self.y = w/2
        self.n = n
        self.pts = []
        self.filter = RandomFilter()


    def import_coordinates(self, pts, z):

        if z > self.z: return []

        for pt in pts:

            # check for malformed point
            if len(pts) < 3: continue

            # random filter
            if not self.filter.pass_filter(): continue

            # trig to re-situate point
            re_fixed = [self.n*(self.z-z)*(pt[0]-self.x)/self.f,
            self.n*(self.z-z)*(pt[1]-self.y)/self.f, z]

            # add to list
            self.pts.append(re_fixed)


    def get_pts(self):

        return np.array(self.pts)
