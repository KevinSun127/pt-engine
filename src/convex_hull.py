from scipy.spatial import ConvexHull
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import open3d as o3d
import os

def csv_to_ssv(input_path, output_dir, file_name):
    # new path to the output file
    new_path = os.path.join(output_dir, file_name)
    if input_path == new_path: return
    # create all intermediate directories
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    # create new space-separated csv
    pd.read_csv(input_path).to_csv(new_path, sep=" ",
    header=False,index=False, index_label=False)

SAVE_PTS = "resources/SAVE_PTS/save.pt.csv"
SAVE_SPACE = "resources/SAVE_MESH/new_save.pt.csv"
SAVE_HULL = "resources/SAVE_MESH/save.stl"

# SAVE_PTS = "resources/SAVE_SOBEL/save.pt.csv"
# SAVE_SPACE = "resources/SAVE_SOBEL_MESH/new_save.pt.csv"
# SAVE_HULL = "new_save.pt.csv"

def display_inlier_outlier(cloud, ind):
    inlier_cloud = cloud.select_down_sample(ind)
    outlier_cloud = cloud.select_down_sample(ind, invert=True)

    print("Showing outliers (red) and inliers (gray): ")
    outlier_cloud.paint_uniform_color([1, 0, 0])
    inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
    o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])

    return inlier_cloud

if __name__ == "__main__":

    # csv_to_ssv(SAVE_PTS, "resources/SAVE_MESH/", "new_save.pt.csv")

    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud(SAVE_SPACE, format="xyz")
    o3d.visualization.draw_geometries([pcd])

    # print("Downsample the point cloud with a voxel of 0.02")
    # voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.02)
    # o3d.visualization.draw_geometries([voxel_down_pcd])
    #
    print("Every 1000th points are selected")
    uni_down_pcd = pcd.uniform_down_sample(every_k_points=100)
    o3d.visualization.draw_geometries([uni_down_pcd])

    print("Statistical oulier removal")
    cl, ind = uni_down_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=1.0)

    cl.estimate_normals()
    o3d.visualization.draw_geometries([cl])

    # for alpha in np.logspace(np.log10(100), np.log10(0.01), num=4):
    #     print(f"alpha={alpha:.3f}")
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(cl, 100)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

    o3d.io.write_triangle_mesh(SAVE_HULL, mesh)
    print('run Poisson surface reconstruction')
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            cl, depth=9)
    print(mesh)
    o3d.visualization.draw_geometries([mesh],
                                      zoom=0.664,
                                      front=[-0.4761, -0.4698, -0.7434],
                                      lookat=[1.8900, 3.2596, 0.9284],
                                      up=[0.2304, -0.8825, 0.4101])

    print("Radius oulier removal")
    cl, ind = voxel_down_pcd.remove_radius_outlier(nb_points=16, radius=0.05)
    display_inlier_outlier(voxel_down_pcd, ind)

#
# pts = np.genfromtxt(SAVE_PTS, delimiter=",")
# hull = ConvexHull(pts)
# pd.DataFrame(hull.points[hull.vertices]).to_csv(SAVE_HULL, index=False, header=False)
