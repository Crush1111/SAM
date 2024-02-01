
import cv2
import numpy as np
import os
from PIL import Image
import argparse


def convert_masks(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            label_image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
            label_image[label_image == 0] = 255
            label_image[label_image != 255] = 0

            output_filename = filename.replace(".png", ".jpg.png")
            output_path = os.path.join(output_folder, output_filename)

            cv2.imwrite(output_path, label_image)

            print(f"处理完成：{filename} -> {output_path}")


def visual_hybrid(image_folder, segment_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(image_folder):
        image_path = os.path.join(image_folder, file_name)
        segment_path = os.path.join(segment_folder, "label.png")

        img = np.array(Image.open(image_path))
        label = np.array(Image.open(segment_path))

        result, result_rgb = visual_hybrid(img, label)

        stacked_image = np.hstack((img, result_rgb))

        output_path = os.path.join(output_folder, f"visualization_{file_name}")

        Image.fromarray(stacked_image).save(output_path)

        print(f"已保存可视化结果至: {output_path}")


def main(input_folder, output_folder_1, image_folder, segment_folder, output_folder_2):
    # 调用 convert_masks 函数
    convert_masks(input_folder, output_folder_1)

    # 调用 visual_hybrid 函数
    visual_hybrid(image_folder, segment_folder, output_folder_2)


if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="处理图像和分割结果的程序")
    parser.add_argument("--input_folder", type=str, help="输入文件夹路径")
    parser.add_argument("--output_folder", type=str, help="输出文件夹路径")
    parser.add_argument("--image_folder", type=str, help="图像文件夹路径")
    parser.add_argument("--segment_folder", type=str, help="分割图像文件夹路径")
    parser.add_argument("--output_folder", type=str, help="输出图像文件夹路径")

    # 解析命令行参数
    args = parser.parse_args()

    # 调用主函数，并传递命令行参数
    main(args.input_folder, args.output_folder, args.image_folder, args.segment_folder, args.output_folder)