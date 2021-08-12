#!/usr/bin/env python
# _*_coding:utf-8_*_
"""
@Time   :  2021/8/10 22:13
@Author :  Qinghua Wang
@Email  :  597935261@qq.com
"""

import math
from collections import namedtuple
from typing import List

import zbar

try:
    import cv2
except ModuleNotFoundError:
    print("Warning,func show_info can not be used when cv2 is not available")

Position = namedtuple("Position", ["left_top", "left_bottom", "right_bottom", "right_top"])


class BarcodeRes:
    """
    BarcodeRes

    text : text of utf-8
    type : barcode type
    location : barcode point list
    rect : bounding box of location
    ori_orientation : zbar inner orientation (Only used for get points)
    orientation : orientation degree
    position : namedtuple with fields ["left_top", "left_bottom", "right_bottom", "right_top"]
    """

    def __init__(self, x: zbar.Symbol):
        self.text = x.data
        self.type = str(x.type)
        self.location = x.location
        self.rect = get_bbox(x.location)
        self.ori_orientation = str(x.orientation)
        if self.ori_orientation == "LEFT":  # for LEFT
            self.position = Position._make([self.location[0], self.location[3], self.location[2], self.location[1]])
        else:
            self.position = Position._make(self.location)

        self.orientation = get_clockwise_orientation(self.position.left_bottom, self.position.left_top, "degree")

    def __repr__(self):
        return str(self.__dict__)


def get_clockwise_orientation(start_p, end_p, return_format="degree"):
    """
    calc clockwise orientation
    :param start_p: start point
    :param end_p: end point
    :param return_format: degree or radian
    :return:
    """
    d_x = end_p[0] - end_p[0]
    d_y = end_p[1] - start_p[1]
    if d_y == 0:
        if d_x >= 0:
            res = math.pi / 2
        else:
            res = -math.pi / 2
    else:
        res = math.atan(d_x / d_y)
    if return_format == "degree":
        res = res / math.pi * 180
    return round(res)


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
    res = [BarcodeRes(x) for x in image]
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
