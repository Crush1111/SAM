import os
import shutil
import zipfile

def split_images(image_directory, target_directory, images_per_subfolder):
    # 遍历原始图片文件夹
    image_files = os.listdir(image_directory)
    total_images = len(image_files)

    # 计算需要创建的子文件夹数量
    num_subfolders = total_images // images_per_subfolder
    if total_images % images_per_subfolder != 0:
        num_subfolders += 1

    # 分割图片并创建子文件夹
    for i in range(num_subfolders):
        subfolder_num = i + 1
        subfolder_name = str(subfolder_num)
        subfolder_path = os.path.join(target_directory, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

        start_index = i * images_per_subfolder
        end_index = min(start_index + images_per_subfolder, total_images)

        # 将照片复制到子文件夹中
        for j in range(start_index, end_index):
            image_file = image_files[j]
            source_path = os.path.join(image_directory, image_file)
            destination_path = os.path.join(subfolder_path, image_file)
            shutil.copy2(source_path, destination_path)

        print(f"Created subfolder {subfolder_name} with {end_index - start_index} images.")

        # 创建子文件夹的压缩包
        subfolder_zip_path = os.path.join(target_directory, f"{subfolder_name}.zip")
        with zipfile.ZipFile(subfolder_zip_path, 'w') as zip_file:
            for root, _, files in os.walk(subfolder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, target_directory)
                    zip_file.write(file_path, arcname)

        print(f"Compressed subfolder {subfolder_name} as {subfolder_zip_path}.")

# 调用函数进行图片分割和压缩
image_directory = "/data/songjiali/Segment-and-Track-Anything/dataset/zhuanhuayuan/image"
target_directory = "/data/songjiali/Segment-and-Track-Anything/dataset/zhuanhuanyuan_seg"
images_per_subfolder = 20

split_images(image_directory, target_directory, images_per_subfolder)

"""import os
import shutil
import zipfile

def split_images(image_directory, target_directory, images_per_subfolder):
    # 遍历原始图片文件夹
    image_files = os.listdir(image_directory)
    total_images = len(image_files)

    # 计算需要创建的子文件夹数量
    num_subfolders = total_images // images_per_subfolder
    if total_images % images_per_subfolder != 0:
        num_subfolders += 1

    # 分割图片并创建子文件夹
    for i in range(num_subfolders):
        subfolder_num = i + 1
        subfolder_name = chr(ord('a') + i)  # 使用字母进行命名
        subfolder_path = os.path.join(target_directory, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

        start_index = i * images_per_subfolder
        end_index = min(start_index + images_per_subfolder, total_images)

        # 将照片复制到子文件夹中
        for j in range(start_index, end_index):
            image_file = image_files[j]
            source_path = os.path.join(image_directory, image_file)
            destination_path = os.path.join(subfolder_path, image_file)
            shutil.copy2(source_path, destination_path)

        print(f"Created subfolder {subfolder_name} with {end_index - start_index} images.")

        # 创建子文件夹的压缩包
        subfolder_zip_path = os.path.join(target_directory, f"{subfolder_name}.zip")
        with zipfile.ZipFile(subfolder_zip_path, 'w') as zip_file:
            for root, _, files in os.walk(subfolder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, subfolder_path)  # 使用相对路径
                    zip_file.write(file_path, arcname)

        print(f"Compressed subfolder {subfolder_name} as {subfolder_zip_path}.")

# 调用函数进行图片分割和压缩
image_directory = "/data/songjiali/Segment-and-Track-Anything/dataset/met_hand/image"
target_directory = "/data/songjiali/Segment-and-Track-Anything/dataset/met_hand_seg"
images_per_subfolder = 100

split_images(image_directory, target_directory, images_per_subfolder)"""