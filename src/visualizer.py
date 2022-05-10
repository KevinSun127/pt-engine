import numpy as np
import pandas as pd
import open3d as o3d
import matplotlib.pyplot as plt
import os

OLD_SAVE_PATH = "resources/pyramid_points/save.pt.csv"
NEW_SAVE_DIR = "resources/pyramid_points_save"
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

def generate_stl(pt_path, pt_dir):
    csv_to_ssv(pt_path, pt_dir, "new_save.pt.csv")
    save_path = os.path.join(pt_dir, "new_save.pt.csv")
    pcd = o3d.io.read_point_cloud(save_path, format='xyz')
    pcd.estimate_normals()
    pcd = pcd.uniform_down_sample(every_k_points=50)
    cl, ind = pcd.remove_statistical_outlier(nb_neighbors=300,std_ratio=.05)
    alpha = .75
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(
        cl, alpha)
    mesh = mesh.compute_vertex_normals()
    mesh = mesh.filter_smooth_simple(number_of_iterations=1)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
    stl_save_path = os.path.join(pt_dir, "print.stl")
    o3d.io.write_triangle_mesh(stl_save_path, mesh)