import argparse
import os
import shutil

import pkg_resources
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


def copy_folder_contents(src_package, src_folder, dest_folder):
    """
    复制 src_package 中 src_folder 的所有内容到 dest_folder。

    :param src_package: 包名
    :param src_folder: 源文件夹路径（相对于包）
    :param dest_folder: 目标文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 遍历源文件夹中的所有文件和子文件夹
    for item in pkg_resources.resource_listdir(src_package, src_folder):
        src_item_path = os.path.join(src_folder, item)
        dest_item_path = os.path.join(dest_folder, item)

        if pkg_resources.resource_isdir(src_package, src_item_path):
            # 如果是文件夹，递归复制
            copy_folder_contents(src_package, src_item_path, dest_item_path)
        else:
            # 如果是文件，直接复制
            with pkg_resources.resource_stream(src_package, src_item_path) as src_file:
                with open(dest_item_path, 'wb') as dest_file:
                    shutil.copyfileobj(src_file, dest_file)
def copy_file(src_package, src_file, dest_folder):
    """
    复制 src_package 中的 src_file 到 dest_folder。

    :param src_package: 包名
    :param src_file: 源文件路径（相对于包）
    :param dest_folder: 目标文件夹路径
    """
    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # 获取源文件的文件名
    file_name = os.path.basename(src_file)
    dest_file_path = os.path.join(dest_folder, file_name)

    # 复制文件
    with pkg_resources.resource_stream(src_package, src_file) as src_file:
        with open(dest_file_path, 'wb') as dest_file:
            shutil.copyfileobj(src_file, dest_file)

def create_gfpt():
    src_package = 'insta360_gfpt'
    src_folder = 'templates/src'
    dest_folder = '.'
    logger.info("create src")
    copy_folder_contents(src_package, src_folder, dest_folder)
    src_folder = 'templates/res'
    dest_folder = '.'
    logger.info("create res")
    copy_folder_contents(src_package, src_folder, dest_folder)
    src_folder = 'templates/tools'
    dest_folder = '.'
    logger.info("create tool")
    copy_folder_contents(src_package, src_folder, dest_folder)
    src_file = 'templates/main.py'
    dest_folder = '.'
    logger.info("create main")
    copy_file(src_package, src_file, dest_folder)

    src_file = 'templates/setting.json'
    dest_folder = '.'
    logger.info("create setting.json")
    copy_file(src_package, src_file, dest_folder)

    pass
if __name__ == "__main__":
    main()