import numpy as np
import pyvista as pv
import pandas as pd

SAVE_FILE = "resources/SAVE_PTS/save.pt.csv"

pts = np.genfromtxt(SAVE_FILE,delimiter=",")
pv.PolyData(pts).plot()
