# 待完成

- 修复compress_images_in_subfolder2函数，实现更小的内存占用以及速度
- 添加仅压缩一张图片功能，可以通过判断输入的路径是否是图片完成

# 已完成

## 文件附加三个参数，可任意顺序
1. 大小(单位mb省略) 文件期望的大小
2. 分辨率（单位像素）文件最大的像素边长
3. overwrite 覆盖源文件

大小和分辨率通过数字大小（一百以内是大小，一百以上是分辨率）区别，同时也可以在后面加上单位

## 实现递归判断文件夹

为简单起见，可以强制启用overwrite参数

# v1 存档

以下是已经弃用的v1版本

```python
#!/bin/python
import os
import shutil
import sys
from PIL import Image
from PIL import ImageOps

def compress_images_in_folder(folder_path, file_size_limit, photo_width_limit):
    # Create the subfolder
    subfolder_path = os.path.join(folder_path, folder_path.split(os.sep)[-1] + "压缩")
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # Copy all images to the subfolder
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy(file_path, subfolder_path)

    # Compress images larger than 5MB in the subfolder
    for file in os.listdir(subfolder_path):
        file_path = os.path.join(subfolder_path, file)
        inital_quality = 90
        compress_time = 1
        # 复制单张图片
        #if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg')):
        original_file_path = os.path.join(folder_path, file)
        #shutil.copy(original_file_path, subfolder_path)
        # 避免不必要的压缩
        if os.path.getsize(original_file_path) > file_size_limit * 1024 * 1024 * 1.5:
            inital_quality -= 5

        if os.path.getsize(original_file_path) > file_size_limit * 1024 * 1024:
            # 如果不够小就减小压缩率重复压缩
            while True:  # 5MB
                # 执行压缩
                print(f"compressing {file} for the {compress_time}th time, quality: {inital_quality}")
                with Image.open(original_file_path) as img:
                    img = img.convert("RGB")  # Convert to RGB if not already (for JPEG)
                    img = ImageOps.exif_transpose(img)
                    # 压缩图片边长
                    if(photo_width_limit > 0):
                        img.thumbnail((photo_width_limit, photo_width_limit))
                    img.save(file_path, "JPEG", quality=inital_quality, optimize=True)
                # 检测文件是否达到尺寸要求
                if os.path.getsize(file_path) > file_size_limit * 1024 * 1024:
                    inital_quality -= 5
                    compress_time += 1
                    # 重新复制单张图片重试压缩
                    # original_file_path = os.path.join(folder_path, file)
                    # shutil.copy(original_file_path, subfolder_path)
                else:
                    break
        else:
            # 满足要求就直接复制，不用压缩
            print(f"copying {file}")
            shutil.copy(original_file_path, subfolder_path)

    print(f"Images copied and compressed in '{subfolder_path}'.")

# Example usage
# Replace "/path/to/your/folder" with the actual folder path you want to process.
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python script.py <folder_path> <limit_size(measure in MB)>")
        #print("或者也可以直接修改下面的目录直接开始")
        #compress_images_in_folder("/home/yuchen/Pictures/12.15 运动会彩排与宿舍楼/运动会彩排/还行")
    elif len(sys.argv) == 2:
        folder_path = sys.argv[1]
        print(f"Start compress, target file size: 4 MB.")
        print(f"You can change it by add a number after folder_path when execute the command")
        compress_images_in_folder(folder_path, 4, 0)
    elif len(sys.argv) == 3:
        folder_path = sys.argv[1]
        limit = float(sys.argv[2])
        print(f"Start compress, target file size: {limit} MB.")
        compress_images_in_folder(folder_path, limit, 0)
```
