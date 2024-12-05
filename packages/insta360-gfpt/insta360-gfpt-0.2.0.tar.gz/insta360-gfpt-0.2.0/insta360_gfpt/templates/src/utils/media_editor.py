# 照片视频处理
import PIL.Image as Image
import os, time
from loguru import logger

def images_eighteen(images):
    images = list(images)
    image_eighteen = [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0]
    images_five = [1, 6, 3, 0, 4, 8, 5, 9, 2, 7]
    eighteen_imgs = []
    eighteen_imgs_zone = []
    for i in range(0, 18):
        if image_eighteen[i] == 1:
            image = images[images_five.pop(0)]
            eighteen_imgs.append(image["path"])
            eighteen_imgs_zone.append(image["zone"])
            imgs_dir = os.path.dirname(image["path"])
        else:
            eighteen_imgs.append("")
            eighteen_imgs_zone.append([])
    return eighteen_imgs, eighteen_imgs_zone, imgs_dir

def images_nine(images):
    images = list(images)
    image_nine = [ 1, 0, 1, 0, 1, 0, 1, 0, 1]
    images_five = [1, 4, 0, 2, 3]
    nine_imgs = []
    nine_imgs_zone = []
    for i in range(0, 9):
        if image_nine[i] == 1:
            image = images[images_five.pop(0)]
            nine_imgs.append(image["path"])
            nine_imgs_zone.append(image["zone"])
            imgs_dir = os.path.dirname(image["path"])
        else:
            nine_imgs.append("")
            nine_imgs_zone.append([])
    return nine_imgs, nine_imgs_zone, imgs_dir
def images_two(images):
    images = list(images)
    two_imgs = []
    two_imgs_zone = []
    for i in range(0, 2):
        image = images[i]
        two_imgs.append(image["path"])
        two_imgs_zone.append(image["zone"])
        imgs_dir = os.path.dirname(image["path"])
    return two_imgs, two_imgs_zone, imgs_dir

def image_zone(image):
    img = Image.open(image)
    # img = Image.open(image)
    width, height = img.size
    # x0, y0, x1, y1
    # 前两个坐标点是左上角坐标
    # 后两个坐标点是右下角坐标
    # width在前， height在后
    x0 = 0
    y0 = 0
    x1 = width
    y1 = height
    box = (x0, y0, x1, y1)
    region = img.crop(box)
    # region.show()
    return region

def image_compose(images, IMAGE_ROW = 3, IMAGE_COLUMN = 6 , width = 3040, height = 3040, Rename = False, num = 0):
    t = time.strftime("%Y%m%d_%H%M%S")
    logger.info(images)
    if IMAGE_ROW == 1:
        images, images_zone, imgs_dir = images_two(images)
    elif IMAGE_ROW == 3 and IMAGE_COLUMN == 3:
        images, images_zone, imgs_dir = images_nine(images)
    else:
        images, images_zone, imgs_dir = images_eighteen(images)
    # 打开一个新的图
    to_image = Image.new('RGB', (IMAGE_COLUMN * width, IMAGE_ROW * height))
    # 循环遍历，把每张图按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            if images[IMAGE_COLUMN * (y - 1) + x - 1]:
                l_x, l_y = images_zone[IMAGE_COLUMN * (y - 1) + x - 1]
                from_image = image_zone(images[IMAGE_COLUMN * (y - 1) + x - 1])
                to_image.paste(from_image, ((x - 1) * width, (y - 1) * height))
                del from_image
    # to_image.show()

    # 保存新图
    if Rename:
        compose_save_path = imgs_dir + f"\\IMG_{t}_03_" + str(num) + ".jpg"
    else:
        compose_save_path = imgs_dir + f"\\{t}.jpg"
    to_image.save(compose_save_path)
    return compose_save_path


if __name__ == "__main__":
    a = [{'path': 'D:\\python\\work\\gfpt\\test_pic2.jpg', 'zone': ['0', '0']}, {'path': 'D:\\python\\work\\gfpt\\test_pic2.jpg', 'zone': ['0', '0']}, {'path': 'D:\\python\\work\\gfpt\\test_pic2.jpg', 'zone': ['0', '0']}, {'path': 'D:\\python\\work\\gfpt\\test_pic2.jpg', 'zone': ['0', '0']}, {'path': 'D:\\python\\work\\gfpt\\test_pic2.jpg', 'zone': ['0', '0']}]
    image_compose(a, IMAGE_ROW = 3, IMAGE_COLUMN = 3 )
