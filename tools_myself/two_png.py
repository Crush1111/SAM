import numpy as np
import os
from PIL import Image

def visual_hybrid(image, segment):
    image = image.astype(float)

    for idx in np.unique(segment):
        if idx == 0:
            continue
        mask = segment == idx
        color_mask = [255, 0, 0] if idx == 1 else [0, 255, 0] if idx == 2 else [0, 0, 255]
        image[mask] = image[mask].reshape(-1, 3) * 0.4 + np.array(color_mask) * 0.6

    return image / 255, image[:, :, ::-1].astype(np.uint8)


# 指定输入图像文件夹的路径
image_folder = r"/home/songjiali/LandMark-1/dist_render/car/car_image"

# 指定分割图像文件夹的路径
segment_folder = r"/home/songjiali/LandMark-1/dist_render/car/car_label"

# 指定输出图像文件夹的路径
output_folder = r"/home/songjiali/LandMark-1/dist_render/car/car_output"

# 确保输出目录存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的原图像文件
for file_name in os.listdir(image_folder):
    image_path = os.path.join(image_folder, file_name)
    segment_path = os.path.join(segment_folder, "label.png")

    # 读取原图像和分割图像
    img = np.array(Image.open(image_path))
    label = np.array(Image.open(segment_path))

    # 应用可视化函数，获取可视化结果
    result, result_rgb = visual_hybrid(img, label)

    # 堆叠原图和分割结果
    stacked_image = np.hstack((img, result_rgb))

    # 生成输出文件路径
    output_path = os.path.join(output_folder, f"visualization_{file_name}")

    # 保存堆叠后的图像
    Image.fromarray(stacked_image).save(output_path)

    print(f"已保存可视化结果至: {output_path}")