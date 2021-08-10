#!/usr/bin/env python
# _*_coding:utf-8_*_
"""
@Time   :  2021/8/10 22:13
@Author :  Qinghua Wang
@Email  :  597935261@qq.com
"""

from typing import List

import zbar

try:
    import cv2
except ModuleNotFoundError:
    print("Warning,func show_info can not be used when cv2 is not available")


class BarcodeRes:
    """
    BarcodeRes
    """

    def __init__(self, text, barcode_type, location):
        self.text = text
        self.barcode_type = barcode_type
        self.location = location
        self.rect = get_bbox(location)

    def __repr__(self):
        return str(self.__dict__)


def get_bbox(p_list):
    """

    :param p_list:
    :return:
    """
    x_list, y_list = [item[0] for item in p_list], [item[1] for item in p_list]
    p_left_top = (min(x_list), min(y_list))
    p_right_bottom = (max(x_list), max(y_list))
    x_center = (p_left_top[0] + p_right_bottom[0]) / 2
    y_center = (p_left_top[1] + p_right_bottom[1]) / 2
    width = p_right_bottom[0] - p_left_top[0]
    height = p_right_bottom[1] - p_left_top[1]
    return x_center, y_center, width, height


def decode(img):
    """
    get BarCode decode result
    :param img: cv2 image (np array)(gray is better)
    :return:
    """
    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')
    height, width = img.shape[:2]
    raw = img.tobytes()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    res = [BarcodeRes(x.data, str(x.type), x.location) for x in image]
    return res


def show_info(barcode_list: List[BarcodeRes], image):
    """

    :param barcode_list:
    :param image:
    :return:
    """
    for barcode in barcode_list:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)),
                      (255, 255, 0), 10)
        cv2.putText(image, barcode.text, (int(x - w / 2), int(y - h / 2)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.imshow("res", image)
    cv2.waitKey()


if __name__ == '__main__':
    image_path = "../test.png"
    img = cv2.imread(image_path)
    print(decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)))
    show_info(decode(cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)), img)
