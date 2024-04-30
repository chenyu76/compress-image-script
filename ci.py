#!/bin/python
import os
import shutil
import sys
from PIL import Image
from PIL import ImageOps


# 递归压缩文件夹里的图片
def compress_images_in_subfolder(
    input_path, output_path, file_size_limit=4, image_resolution_limit=0
):
    subfolders = list_subfolders(input_path)
    for folder in subfolders:
        compress_images_in_folder(
            folder,
            folder.replace(input_path, output_path),
            file_size_limit,
            image_resolution_limit,
        )
    return 0


# 递归压缩文件夹里的图片 方法2，应该更快一点，可惜不能用，需要修复
def compress_images_in_subfolder2(
    input_path, output_path, file_size_limit=4, image_resolution_limit=0
):
    for item in os.listdir(input_path):
        if os.path.isdir(os.path.join(input_path, item)):
            compress_images_in_subfolder(
                item,
                item.replace(input_path, output_path),
                file_size_limit,
                image_resolution_limit,
            )
        elif os.path.isfile(os.path.join(input_path, item)):
            compress_image(
                input_path, output_path, item, file_size_limit, image_resolution_limit
            )
    return 0


# 压缩指定文件夹里的图片
def compress_images_in_folder(
    input_path, output_path, file_size_limit=4, image_resolution_limit=0
):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    for file in os.listdir(input_path):
        if os.path.isfile(os.path.join(input_path, file)):
            compress_image(
                input_path, output_path, file, file_size_limit, image_resolution_limit
            )
    return 0


def compress_image(
    input_path, output_path, image_name, file_size_limit=4, image_resolution_limit=0
):
    """压缩单张图片

    Args:
    image_path (str): 原始图片的路径（不包含文件名）
    output_path : 压缩后图片保存路径（不包含文件名）
    image_name : 图片的文件名
    file_size_limit: 限制的文件大小
    photo_resolution_limit： 限制的图片尺寸

    Returns:
    0： 无异常
    -1： 不是图片
    """
    image_path = os.path.join(input_path, image_name)
    image_output_path = os.path.join(output_path, image_name)
    file_size_limit_MB = file_size_limit * 1024 * 1024

    # 每压缩一张打印一个点
    # print(".",end="")

    # 检测是否是图片
    if not (
        os.path.isfile(image_path)
        and image_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
    ):
        return -1

    # 检测图片是否满足大小，满足就直接拷贝
    if os.path.getsize(image_path) < file_size_limit_MB and output_path != input_path:
        print(f"\rcopying {image_name}", end="")
        shutil.copy(image_path, image_output_path)
        return 0

    # 图片需要压缩
    with Image.open(image_path) as img:
        inital_quality = 90
        compress_time = 1

        # 避免不必要的压缩
        if os.path.getsize(image_path) > file_size_limit_MB * 1.5:
            inital_quality -= 5

        # 保留exif信息
        exif = "0"
        if "exif" in img.info.keys():
            exif = img.info["exif"]

        # 压缩图片尺寸
        if image_resolution_limit > 0:
            img.thumbnail((image_resolution_limit, image_resolution_limit))
        img = img.convert("RGB")  # Convert to RGB if not already (for JPEG)
        img = ImageOps.exif_transpose(img)
        while True:
            print(
                f"\rcompressing {image_name} {compress_time}th time, quality: {inital_quality}",
                end="",
            )
            if exif == "0":
                img.save(
                    image_output_path, "JPEG", quality=inital_quality, optimize=True
                )
            else:
                img.save(
                    image_output_path,
                    "JPEG",
                    quality=inital_quality,
                    optimize=True,
                    exif=exif,
                )
            inital_quality -= 5
            compress_time += 1
            if os.path.getsize(image_output_path) < file_size_limit_MB:
                break

    return 0


def list_subfolders(directory):
    """Recursively returns a list of all subfolders in the specified directory.

    Args:
    directory (str): The path of the directory to list subfolders from.

    Returns:
    list: A list containing the paths of all subfolders.
    """
    subfolders = [directory]
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            subfolders.append(os.path.join(root, dir))
    return subfolders

# 统计一个字符串从头开始数，出现的数字（包括小数点）次数
def digit_count(str, num = 0):
    return digit_count(str[1:], num+1) if str[0] in '1234567890.' else num

if __name__ == "__main__":
    help_information = """
    使用说明（by ChatGPT 4）：

    这是一个图片压缩工具，可以压缩指定文件夹中的所有图片。您可以设置图片的最大体积和分辨率，并选择是否覆盖原图或保存到不同的文件夹。

    命令行参数：

    目录路径: 指定要压缩的图片所在的文件夹路径。
    数字参数:
    0 < 数字 < 10: 设置图片的最大体积（以MB为单位）。
    数字 > 100: 设置图片的最大分辨率（以像素为单位）。
    -o, --overwrite: 覆盖原始图片。
    -r, --recursive: 递归压缩子文件夹中的图片。
    -h, --help: 显示此帮助信息。
    -v, --version: 显示程序版本。

    使用示例：
    python ci.py /path/to/folder --recursive --overwrite 5 1024
    上述命令将递归压缩'/path/to/folder'目录下的图片，覆盖原图，设置图片最大体积为5MB，最大分辨率为1024x1024像素。

    注意：
    - 必须提供至少一个文件夹路径。
    - 如果未设置大小和分辨率限制，程序将使用默认设置(4MB，无分辨率限制)。
    - 参数无先后顺序限制
    """
    version = "2.1"
    folder_path = "0"
    output_folder_path = "0"
    limit_size = 0.25
    limit_resolution = 0
    overwrite = False
    recursive = False
    if len(sys.argv) == 1:
        print(help_information)
        exit()

    for arg in sys.argv[1:]:
        dig_num = digit_count(arg) if arg[0] != '.' else 0 # 相对路径会遇到第一个是点的问题
        if dig_num:  # 这里需要添加小数点和mb p 的判断
            f_arg = float(arg[:dig_num])
            if 0 < f_arg < 10:
                limit_size = f_arg
            elif 100 < f_arg:
                limit_resolution = int(f_arg)
        else:
            if os.path.isdir(arg):
                folder_path = arg
            elif arg == "--overwrite":
                overwrite = True
            elif arg == "--recursive":
                recursive = True
            elif arg == "--help":
                print(help_information)
            elif arg == "--version":
                print("version:" + version)
            elif arg[0] == "-":
                for c in arg[1:]:
                    if c == "o":
                        overwrite = True
                    elif c == "r":
                        recursive = True
                    elif c == "h":
                        print(help_information)
                    elif c == "v":
                        print("version:" + version)

    if folder_path == "0":
        print("必须提供需要压缩的图片的目录！")
        exit()

    if overwrite:
        output_folder_path = folder_path
    else:
        if folder_path[-1] == os.sep:
            folder_path = folder_path[:-1]
        output_folder_path = folder_path + "_压缩"
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

    # 打印配置信息
    print(f'将压缩文件夹 "{folder_path}" 里的图片')
    if overwrite:
        print("覆盖此文件夹中原始图片")
    else:
        print(f'保存至 "{output_folder_path}" ')
    print(f"限制大小{limit_size}MB，", end="")
    if limit_resolution == 0:
        print("不限制尺寸")
    else:
        print(f"图片尺寸限制为{limit_resolution}x{limit_resolution}以内")

    if recursive:
        compress_images_in_subfolder(
            folder_path, output_folder_path, limit_size, limit_resolution
        )
    else:
        compress_images_in_folder(
            folder_path, output_folder_path, limit_size, limit_resolution
        )

    print("完成")
