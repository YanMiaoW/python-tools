import os
import random
import shutil

import click
import cv2 as cv
import numpy as np


'''
example:
python image_organize.py -r "E:\Desktop\image_spyder" -s "E:\Desktop\image_fix\2020-06-15\road_disease"
python image_organize.py -r "E:\Desktop\image_spyder" -s "E:\Desktop\image_fix\2020-06-15\road_disease -t 50"
'''


@click.command()
@click.option('-r', '--images-root', type=str, required=True,
              help="要整理的图片根目录")
@click.option('-s', '--save-path', type=str, required=True,
              help="整理后保存的路径")
@click.option('-t', '--test-number', default=None, type=int,
              help="如果要将图片分成训练图片和测试图片，需要设置测试图片数量")
def main(images_root, save_path, test_number):
    '''
    输入图片根目录，该脚本会在这个目录下的文件夹和子文件夹，遍历找到所有的图片，打乱顺序，转换图片格式，重命名，放入保存路径。
    '''

    # 清空保存文件夹
    if os.path.exists(save_path):
        shutil.rmtree(save_path)

    # 生成保存文件夹
    os.mkdir(save_path)
    if test_number:
        os.mkdir(save_path + '/test')
        os.mkdir(save_path + '/train')

    def iter_folder_tree(rootdir):
        '''遍历整个文件夹树，将所有图片文件的路径提取出来'''
        
        # 路径数组
        paths = []

        # 遍历文件夹，找出所有的图片
        for subdir, dirs, files in os.walk(rootdir):
            for file in files:
                path = os.path.join(subdir, file)
                if os.path.basename(path).endswith('.jpg') or \
                        os.path.basename(path).endswith('.png') or \
                        os.path.basename(path).endswith('.bmp'):
                    paths.append(path)

        # 打乱路径顺序
        random.shuffle(paths)

        return paths
    
    # 图片id
    image_id = 1

    # 测试图片id
    test_image_id = 1

    for image_path in iter_folder_tree(images_root):
        # 打印图片路径
        print(image_path)

        # 读取图片
        img = imread(image_path)
        if img is None:
            print(image_path, '读取失败')
            continue

        # 存入测试图片
        if test_number and test_image_id <= test_number:
            new_image_test_path = f'{save_path}/test/{str(test_image_id).zfill(5)}.jpg'
            cv.imwrite(new_image_test_path, img)
            test_image_id += 1
            continue

        # 存入训练图片
        if test_number:
            new_image_path = f'{save_path}/train/{str(image_id).zfill(5)}.jpg'
        else:
            new_image_path = f'{save_path}/{str(image_id).zfill(5)}.jpg'
        cv.imwrite(new_image_path, img)
        
        image_id += 1


def imread(path):
    '''opencv的imread方法对中文路径的支持不好，用此函数读取图片'''
    img = cv.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    return img


if __name__ == '__main__':
    main()
