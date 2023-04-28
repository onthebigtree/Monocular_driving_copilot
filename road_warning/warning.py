import cv2
import json
import numpy as np

# 定义预警阈值
distance_threshold = 100  # 以像素为单位

def depth_based_warning(depth_image_path = "../system_db/id_1/1_disp.jpeg" , output_json_path = "../system_db/id_1/output.json"):
    # 读取深度图像
    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_ANYDEPTH)

    # 判断深度图像是否存在
    if depth_image is None:
        raise FileNotFoundError("深度图像不存在或无法读取")

    # 将深度图像分为三个部分（左、中、右）
    image_height, image_width = depth_image.shape
    left_image = depth_image[:, :image_width//3]
    center_image = depth_image[:, image_width//3: 2*image_width//3]
    right_image = depth_image[:, 2*image_width//3:]

    # 获取每个区域的最小距离
    left_min_distance = np.min(left_image)
    center_min_distance = np.min(center_image)
    right_min_distance = np.min(right_image)

    # 判断是否存在小于阈值的最小距离
    warning = False
    direction = None
    if left_min_distance < distance_threshold:
        warning = True
        direction = "left"
    elif center_min_distance < distance_threshold:
        warning = True
        direction = "center"
    elif right_min_distance < distance_threshold:
        warning = True
        direction = "right"

    message = "warning!" if warning else "safe."

    # 将输出结果保存为JSON格式，并将其写入指定的文件路径中
    output_data = {
        "distance_threshold": distance_threshold,
        "min_distances": {
            "left": int(left_min_distance),
            "center": int(center_min_distance),
            "right": int(right_min_distance)
        },
        "warning": warning,
        "direction": direction,
        "message": message
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
