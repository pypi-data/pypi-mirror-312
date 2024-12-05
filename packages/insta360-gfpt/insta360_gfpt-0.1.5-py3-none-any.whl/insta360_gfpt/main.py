import argparse
import os
import shutil
from loguru import logger
def main():
    parser = argparse.ArgumentParser(description='创建 insta360 gfpt 项目')
    parser.add_argument('--type', type=str, help='The command to execute')
    parser.add_argument('--option', type=str, help='An optional argument')

    args = parser.parse_args()

    if args.type == 'new':
        create_gfpt()
        print(f"new project, {args.option}!")
    elif args.type == 'old':
        print(f"exist project: {args.option}")
    else:
        print("Unknown command")


def copy_folder_contents(src_folder, dest_folder):
    """
    复制 src_folder 中的所有内容到 dest_folder。

    :param src_folder: 源文件夹路径
    :param dest_folder: 目标文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 遍历源文件夹中的所有文件和子文件夹
    for item in os.listdir(src_folder):
        src_item = os.path.join(src_folder, item)
        dest_item = os.path.join(dest_folder, item)

        if os.path.isdir(src_item):
            # 如果是文件夹，递归复制
            shutil.copytree(src_item, dest_item)
        else:
            # 如果是文件，直接复制
            shutil.copy2(src_item, dest_item)
def copy_file(src_file, dest_folder):
    """
    复制 src_file 到 dest_folder。

    :param src_file: 源文件路径
    :param dest_folder: 目标文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 获取源文件的文件名
    file_name = os.path.basename(src_file)
    dest_file = os.path.join(dest_folder, file_name)

    # 复制文件
    shutil.copy2(src_file, dest_file)

def create_gfpt():
    src_folder = 'templates/src'
    dest_folder = '.'
    logger.info("create src")
    copy_folder_contents(src_folder, dest_folder)
    src_folder = 'templates/res'
    dest_folder = '.'
    logger.info("create res")
    copy_folder_contents(src_folder, dest_folder)
    src_folder = 'templates/tools'
    dest_folder = '.'
    logger.info("create tool")
    copy_folder_contents(src_folder, dest_folder)
    src_file = 'templates/main.py'
    dest_folder = '.'
    logger.info("create main")
    copy_file(src_file, dest_folder)

    src_file = 'templates/setting.json'
    dest_folder = '.'
    logger.info("create setting.json")
    copy_file(src_file, dest_folder)

    pass
if __name__ == "__main__":
    main()