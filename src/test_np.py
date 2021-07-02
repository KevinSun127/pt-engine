import numpy as np

img_col = np.array([[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1],
[0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,1,1,0,1]])
diff = np.argwhere(img_col == 1)
# print(np.where(diff[1:] - diff[:-1] != 1)[0])
# print(np.split(img_col, np.where(diff[1:] - diff[:-1] != 1)[0]))
clusters = np.split(diff, np.where(diff[1:,1] - diff[:-1,1] != 1)[0]+1)
pts = []
for cluster in clusters:
    if len(cluster) > 5:
        pts.append(cluster[0])
        pts.append(cluster[-1])

print(pts)
