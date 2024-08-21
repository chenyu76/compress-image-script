#!/bin/python
import os
import sys
import shutil
from PIL import Image


# 将webp和png转为jpg，保留目录结构
def convert_image_to_jpg(source_folder):
    # 目标文件夹是原文件夹名后加"_jpg"
    target_folder = f"{source_folder}_jpg"

    for root, dirs, files in os.walk(source_folder):
        # 计算当前遍历的目录相对于源文件夹的相对路径
        rel_path = os.path.relpath(root, source_folder)
        # 构建目标目录的路径
        target_dir = os.path.join(target_folder, rel_path)
        # 如果目标目录不存在，创建它
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for file in files:
            # 源文件完整路径
            source_file = os.path.join(root, file)
            # 目标文件完整路径
            target_file = os.path.join(target_dir, file)

            # 转换.webp和.png文件为.jpg
            if file.lower().endswith((".webp", ".png")):
                # 改变文件扩展名为.jpg
                target_file = os.path.splitext(target_file)[0] + ".jpg"
                try:
                    with Image.open(source_file) as img:
                        img.convert("RGB").save(target_file, "jpeg")
                    print(f"Converted {source_file} to {target_file}")
                except Exception as e:
                    print(f"Error converting {source_file}: {e}")
            else:
                # 对于非.webp和非.png文件，直接复制
                try:
                    shutil.copy2(source_file, target_file)
                    print(f"Copied {source_file} to {target_file}")
                except Exception as e:
                    print(f"Error copying {source_file}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <source_folder_path>")
        sys.exit(1)
    source_folder = sys.argv[1]
    convert_image_to_jpg(source_folder)
