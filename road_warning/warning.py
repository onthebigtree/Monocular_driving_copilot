# 迭代思路
# 简单预警，但是经常会因为道路干扰预警效果

# 方法1，使用语义分割识别物品，再对物品进行深度识别
# 失败，语义分割识别物品效果不好，且需要大量数据集，运算速度慢

# 方法2，使用阈值过滤：通过设置一个合适的阈值，我们可以排除路面上的距离值。例如，您可以设置一个最小距离阈值，当距离小于这个阈值时，我们认为这些像素可能属于路面，将其过滤掉：
# 实现代码：
        #min_distance_threshold = 50
        # depth_image_filtered = np.where(depth_image > min_distance_threshold, depth_image, np.inf)
# 失败，阈值过滤效果不好，而且不同的地方需要不同的参数，鲁棒性较弱

# 方法3，裁剪深度图像：我们可以选择裁剪掉深度图像的下半部分，因为路面主要出现在图像的下半部分。这样可以减少路面对预警系统的干扰
        #depth_image = depth_image[:image_height//2, :]
# 效果还能接受

# 为了更好实现道路和周围效果的屏蔽
# 采用了ROI（Region of Interest）技术，即感兴趣区域
# 测试下来还是有比较多的干扰，比如路边的树木，路边的建筑物，路边的车辆等，以及会有一些单点识别错误的情况
# 因此ROI规划了图像四周的边界，且对深度图像做了平滑处理




import cv2
import json
import numpy as np

# 定义预警阈值级别
distance_thresholds = {
    "low": 70,  # 以像素为单位
    "medium": 40,
    "high": 25
}

def draw_red_circle(image, position, radius=5, color=(0, 0, 255), thickness=-1):
    cv2.circle(image, position, radius, color, thickness)

# 对monodepth2的输出结果预处理：



def set_roi(depth_image):
    image_height, image_width = depth_image.shape

    # 设置ROI的边界
    roi_top = 5 * image_height // 100
    roi_bottom = 90 * image_height // 100
    roi_left = 5 * image_width // 100
    roi_right = 95 * image_width // 100

    # 获取ROI区域
    depth_image_roi = depth_image[roi_top:roi_bottom, roi_left:roi_right]

    return depth_image_roi

# 平滑处理
def sliding_window(image, window_size):
    height, width = image.shape
    output = np.zeros((height - window_size + 1, width - window_size + 1))
    for i in range(height - window_size + 1):
        for j in range(width - window_size + 1):
            output[i, j] = np.mean(image[i:i + window_size, j:j + window_size])
    return output

# 获取预警级别
def get_warning_level(distance):
    if distance < distance_thresholds["high"]:
        return "high"
    elif distance < distance_thresholds["medium"]:
        return "medium"
    elif distance < distance_thresholds["low"]:
        return "safe"

def depth_based_warning(depth_image_path = "../system_db/id_1/1_disp.jpeg" , output_json_path = "../system_db/id_1/output.json"):
    # 读取深度图像
    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_ANYDEPTH)

    # 将monodepth2生成的深度恢复为正常值
    depth_image = -depth_image

    scale_factor = 1  # 根据实际情况设置适当的缩放因子
    depth_image = depth_image * scale_factor

    min_depth = 1  # 设置最小深度值
    max_depth = 1000  # 设置最大深度值
    depth_image = np.where((depth_image >= min_depth) & (depth_image <= max_depth), depth_image, np.inf)



    # 判断深度图像是否存在
    if depth_image is None:
        raise FileNotFoundError("深度图像不存在或无法读取")

    # 调用ROI函数
    depth_image_roi = set_roi(depth_image)

    # 使用depth_image_roi替换原始depth_image
    depth_image = depth_image_roi

    # 保存ROI后的深度图像
    cv2.imwrite("depth_image_roi.png", depth_image)

    # 将深度图像分为三个部分（左、中、右）
    image_height, image_width = depth_image.shape
    left_image = depth_image[:, :image_width//3]
    center_image = depth_image[:, image_width//3: 2*image_width//3]
    right_image = depth_image[:, 2*image_width//3:]

    # 设置滑动窗口大小
    window_size = 5

    # 对每个区域应用滑动窗口
    left_image_smoothed = sliding_window(left_image, window_size)
    center_image_smoothed = sliding_window(center_image, window_size)
    right_image_smoothed = sliding_window(right_image, window_size)

    # 获取每个区域的最小平均距离及其位置
    left_min_distance = np.min(left_image_smoothed)
    center_min_distance = np.min(center_image_smoothed)
    right_min_distance = np.min(right_image_smoothed)

    # 根据距离判断预警级别
    left_warning_level = get_warning_level(left_min_distance)
    center_warning_level = get_warning_level(center_min_distance)
    right_warning_level = get_warning_level(right_min_distance)

    # 将输出结果保存为JSON格式，并将其写入指定的文件路径中
    output_data = {
        "distance_thresholds": distance_thresholds,
        "min_distances": {
            "left": int(left_min_distance),
            "center": int(center_min_distance),
            "right": int(right_min_distance)
        },
        "warning_levels": {
            "left": left_warning_level,
            "center": center_warning_level,
            "right": right_warning_level
        }
    }
    with open(output_json_path, "w") as f:
        json.dump(output_data, f)

if __name__ == "__main__":
    # 指定深度图像路径
    depth_image_path = "../system_db/id_1/1_disp.jpeg"
    # 指定输出JSON文件的路径
    output_json_path = "../system_db/id_1/1.json"
    # 运行行进预警功能并保存输出到指定文件
    depth_based_warning(depth_image_path, output_json_path)
    with open(output_json_path, "r") as f:
        output_data = json.load(f)
    print(output_data)





