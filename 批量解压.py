import os
import zipfile
import shutil

# 支持的图片格式
IMAGE_EXTENSIONS = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.webp']

def find_zip_files(directory):
    """ 递归搜索目录下的所有 .zip 文件 """
    zip_files = []
    for root, dirs, files in os.walk(directory):
        print(f"Searching in directory: {root}")  # 打印当前搜索的目录
        for file in files:
            if file.endswith('.zip'):
                full_path = os.path.join(root, file)
                print(f"Found .zip file: {full_path}")  # 打印找到的 .zip 文件
                zip_files.append(full_path)
    return zip_files

def extract_images_from_zip(zip_path, output_dir):
    """ 解压 .zip 文件并提取所有支持的图片格式 """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for member in zip_ref.namelist():
            if any(member.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                # 提取文件
                zip_ref.extract(member, path=output_dir)
                # 移动文件到目标文件夹
                source_file = os.path.join(output_dir, member)
                target_file = os.path.join(output_dir, os.path.basename(member))
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.move(source_file, target_file)
                print(f"Extracted and moved: {target_file}")  # 打印提取和移动的文件

def main():
    img_directory = 'img'  # 源文件夹
    img_all_directory = r'C:\Users\lenovo\Desktop\图片\网图\36壁纸'  # 目标文件夹

    # 创建目标文件夹如果它不存在
    os.makedirs(img_all_directory, exist_ok=True)

    # 查找所有 .zip 文件
    zip_files = find_zip_files(img_directory)

    # 处理每个 .zip 文件
    for zip_file in zip_files:
        print(f"Processing {zip_file}")
        extract_images_from_zip(zip_file, img_all_directory)

if __name__ == '__main__':
    main()