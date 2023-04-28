import numpy as np

# 读取npy文件
depth_image = np.load('/Users/yewlne/Desktop/monodepth2/monodepth2-master/assets/test_disp.npy')

# 获取图像位数
print(depth_image.dtype)

# 获取图像类型
print(depth_image.shape)

# 获取通道数（深度图像只有一个通道）
print(depth_image.shape[-1])

depth_image = depth_image[..., np.newaxis]  # 增加一个通道维度
depth_image = depth_image.transpose((2, 0, 1))  # 将通道维调整到最前面
