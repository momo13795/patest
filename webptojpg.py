import os
import subprocess

def convert_webp_to_jpg(input_file, output_file):
    # 构建 ffmpeg 命令
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',  # 覆盖已存在文件
        '-i', input_file,  # 输入文件路径
        '-q:v', '2',  # 设置输出图片质量，可根据需要调整
        output_file  # 输出文件路径
    ]
    # ffmpeg_cmd = ['ffmpeg', '-i', input_file, output_file]
    subprocess.run(ffmpeg_cmd)

def batch_convert_webp_to_jpg(input_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有 webp 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".webp"):
            input_path = os.path.join(input_folder, filename)
            print('input-path: %s' % (input_path))

            # 生成输出文件的文件名，将后缀改为 .jpg
            output_filename = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(output_folder, output_filename)
            print('out-path: %s' % (output_path))

            # 转换 webp 到 jpg
            convert_webp_to_jpg(input_path, output_path)

def main():
    # 指定 WebP 文件所在的目录路径
    webp_directory = 'C:\\Users\\mark\\Downloads\\linshi'
    jpg_directory = 'C:\\Users\\mark\\Downloads\\linshi\\jpg'

    # 获取目录下的所有 WebP 文件
    webp_files = [file for file in os.listdir(webp_directory) if file.lower().endswith('.webp')]

    # 转换每个 WebP 文件为 JPG
    for webp_file in webp_files:
        webp_file_path = os.path.join(webp_directory, webp_file)
        print('web-path: %s' % (webp_file_path))

        jpg_file = os.path.splitext(webp_file)[0] + '.jpg'
        jpg_file_path = os.path.join(jpg_directory, jpg_file)
        print('file-path: %s' % (jpg_file_path))

        convert_webp_to_jpg(webp_file_path, jpg_file_path)

if __name__ == "__main__":
    # main()
    # 输入 webp 文件夹路径
    webp_folder = "H:\\webtojpg\\base"

    # 输出 jpg 文件夹路径
    jpg_folder = "H:\\webtojpg\\jpg"

    # 批量转换 webp 到 jpg
    batch_convert_webp_to_jpg(webp_folder, jpg_folder)
