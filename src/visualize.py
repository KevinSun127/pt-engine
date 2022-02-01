import numpy as np
import pandas as pd
import open3d as o3d
import matplotlib.pyplot as plt
import os

OLD_SAVE_PATH = "resources/SAVE_SOBEL/save.pt.csv"
NEW_SAVE_DIR = "resources/SAVE_SOBEL_MESH"
NEW_SAVE_NAME = "new_save.pt.csv"

# What want to learn from this package:
# 1. Import Point cloud
# 2. Visualize Point Cloud
# 3. Create Mesh
    # 3.a. Poisson Reconstruction
    # 3.b. Ball Rolling
    # 3.c. Reduce Clusters
# 4. Export Mesh

# Order:
# 1 -> 2 -> 4 -> 3


# comma-separated file to space-separated file
def csv_to_ssv(input_path, output_dir, file_name):
    # new path to the output file
    new_path = os.path.join(output_dir, file_name)
    if input_path == new_path: return
    # create all intermediate directories
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    # create new space-separated csv
    pd.read_csv(input_path).to_csv(new_path, sep=" ",
    header=False,index=False, index_label=False)

csv_to_ssv(OLD_SAVE_PATH, NEW_SAVE_DIR, NEW_SAVE_NAME)
save_path = os.path.join(NEW_SAVE_DIR, NEW_SAVE_NAME)
pcd = o3d.io.read_point_cloud(save_path, format='xyz')
pcd.estimate_normals()
o3d.visualization.draw_geometries([pcd])
# o3d.io.write_point_cloud("save.pcd", pcd)

radii = [1, 2, 3, 4]
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
    pcd, o3d.utility.DoubleVector(radii))
o3d.visualization.draw_geometries([rec_mesh])
# o3d.io.write_triangle_mesh("copy.ply", rec_mesh)

print('run Poisson surface reconstruction')
with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=12)
print(mesh)
o3d.visualization.draw_geometries([mesh],
                                  zoom=0.664,
                                  front=[-0.4761, -0.4698, -0.7434],
                                  lookat=[1.8900, 3.2596, 0.9284],
                                  up=[0.2304, -0.8825, 0.4101])

print('visualize densities')
densities = np.asarray(densities)
density_colors = plt.get_cmap('plasma')(
    (densities - densities.min()) / (densities.max() - densities.min()))
density_colors = density_colors[:, :3]
density_mesh = o3d.geometry.TriangleMesh()
density_mesh.vertices = mesh.vertices
density_mesh.triangles = mesh.triangles
density_mesh.triangle_normals = mesh.triangle_normals
density_mesh.vertex_colors = o3d.utility.Vector3dVector(density_colors)
o3d.visualization.draw_geometries([density_mesh],
                                  zoom=0.664,
                                  front=[-0.4761, -0.4698, -0.7434],
                                  lookat=[1.8900, 3.2596, 0.9284],
                                  up=[0.2304, -0.8825, 0.4101])

print('remove low density vertices')
vertices_to_remove = densities < np.quantile(densities, 0.25)
mesh.remove_vertices_by_mask(vertices_to_remove)
print(mesh)
o3d.visualization.draw_geometries([mesh])

# pcd = o3d.io.read_point_cloud("save.pcd")
# o3d.visualization.draw_geometries([pcd])
