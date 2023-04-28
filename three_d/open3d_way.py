import open3d as o3d
import matplotlib.pyplot as plt
import numpy as np

def Read_Path():
    # 读取彩色图像和深度图像
    rgb_path = '../system_db/id_1/1.png'
    depth_path = '../system_db/id_1/1_disp.jpeg'
    color_raw = o3d.io.read_image(rgb_path)
    depth_raw = o3d.io.read_image(depth_path)
    return color_raw, depth_raw

def RGBD(color_raw, depth_raw):
    # 将彩色图像和深度图像转换为RGBD图像，并设置深度图像的比例因子和截断值
    #depth_scale指示将原始深度值乘以的比例因子，以将其转换为实际深度值。
    #例如，如果深度图像中的每个像素值都乘以1000.0，则可以使用1000.0作为depth_scale参数
    depth_scale = 1
    #depth_trunc是一个截断参数，用于限制深度值的最大值。任何超过该值的深度值都将被截断为最大深度值
    depth_trunc = 30
    #convert_rgb_to_intensity参数指示是否将彩色图像转换为强度图像。 
    #如果设置为True，则将使用彩色图像的亮度值作为强度值。
    #如果设置为False，则仅使用深度图像来生成点云。
    convert_rgb_to_intensity = False
    #是包含彩色图像和深度图像的RGBD图像对象。
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw, depth_scale=depth_scale, depth_trunc=depth_trunc, convert_rgb_to_intensity=convert_rgb_to_intensity)
    return rgbd_image


def Show_RGBD(rgbd_image):
    # 显示RGBD图像的彩色和深度部分
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(rgbd_image.color)
    ax1.set_title('RGB')
    ax2.imshow(rgbd_image.depth)
    ax2.set_title('Depth')
    plt.show()
    
color_raw, depth_raw = Read_Path()
rgbd_image = RGBD(color_raw, depth_raw)

# 调试专用
# Show_RGBD(rgbd_image)  
# print(type(ply))
# print(type(camera))

# 从RGBD图像创建点云
camera = o3d.camera.PinholeCameraIntrinsic(o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault)
ply = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, camera)


# 沿x轴翻转点云，以便与OpenCV中的坐标系对应
flip_transform = np.eye(4)
flip_transform[1, 1] = -1
ply.transform(flip_transform)

# 使用Open3D库中的write_point_cloud函数将点云对象写入ply文件
o3d.io.write_point_cloud("../system_db/id_1/1.ply", ply)

# 可视化点云
# o3d.visualization.draw_geometries([ply])