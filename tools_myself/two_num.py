import cv2
import os

# 指定输入文件夹路径
input_folder = "/data/songjiali/Segment-and-Track-Anything/tracking_results"

# 指定输出文件夹路径
output_folder = "/data/songjiali/Segment-and-Track-Anything/tracking_two_num_result/zhuanhuanyuan"

# 确保输出文件夹存在
os.makedirs(output_folder, exist_ok=True)

# 遍历输入文件夹中的所有文件夹
for folder_name in os.listdir(input_folder):
    folder_path = os.path.join(input_folder, folder_name)

    # 检查文件夹是否以阿拉伯数字命名
    if folder_name.isdigit():
        # 构建阿拉伯数字_masks文件夹的路径
        masks_folder = os.path.join(folder_path, f"{folder_name}_masks")

        # 检查阿拉伯数字_masks文件夹是否存在
        if os.path.exists(masks_folder) and os.path.isdir(masks_folder):
            # 遍历阿拉伯数字_masks文件夹中的所有文件
            for filename in os.listdir(masks_folder):
                if filename.endswith(".png"):
                    # 构建输入文件的完整路径
                    input_path = os.path.join(masks_folder, filename)

                    # 读取输入图像
                    label_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

                    # 将动态物体区域设为0，其余区域设为255
                    label_image[label_image == 0] = 255
                    label_image[label_image != 255] = 0

                    # 构建输出文件的完整路径
                    # 将后缀 ".png" 改为 ".jpg.png"
                    output_filename = filename.replace(".png", ".jpg.png")
                    output_path = os.path.join(output_folder, output_filename)

                    # 保存为与输入文件同名的 PNG 文件
                    cv2.imwrite(output_path, label_image)

                    print(f"处理完成：{filename} -> {output_path}")