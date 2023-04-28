import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

def create_point_cloud(rgb_path = "../system_db/id_1/1.png", depth_path = "../system_db/id_1/1_disp.jpeg", output_path = "../system_db/id_1/1.ply"):
    color_raw = o3d.io.read_image(rgb_path)
    depth_raw = o3d.io.read_image(depth_path)
    
    depth_scale = 1
    depth_trunc = 30
    convert_rgb_to_intensity = False
    
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(
        color_raw, depth_raw, depth_scale=depth_scale, depth_trunc=depth_trunc, 
        convert_rgb_to_intensity=convert_rgb_to_intensity)
    
    camera = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
    ply = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera)
    
    flip_transform = np.eye(4)
    flip_transform[1, 1] = -1
    ply.transform(flip_transform)
    
    o3d.io.write_point_cloud(output_path, ply)
    
    return ply

ply = create_point_cloud()
