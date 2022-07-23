# !/usr/bin/env python
# _*_coding:utf-8_*_
"""
@Time   :  2022/7/23 10:51
@Author :  Qinghua Wang
@Email  :  597935261@qq.com
"""
from unittest import TestCase

import cv2

from zbar_helper.utils import decode


class Test(TestCase):
    def setUp(self) -> None:
        self.expected_text_list = None
        self.real_text_list = None

    def tearDown(self) -> None:
        self.assertEqual(self.expected_text_list, self.real_text_list)

    def test_qr_code(self):
        self.img_path = "./test.png"
        self.expected_text_list = ['https://developer.ibm.com/exchanges/data/all/airline/']
        img = cv2.imread(self.img_path)
        res = decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        self.real_text_list = [item.text for item in res]

    def test_bar_code(self):
        self.img_path = "./bar.png"
        self.expected_text_list = ['6937147252044']
        img = cv2.imread(self.img_path)
        res = decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        self.real_text_list = [item.text for item in res]

    def test_bar_code2(self):
        self.img_path = "./bar2.png"
        self.expected_text_list = ['889368850000BB1',
                                   '889368850000BB2',
                                   '889368850000BB3',
                                   '889368850000BB4',
                                   '889368850000BB5']
        img = cv2.imread(self.img_path)
        res = decode(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        self.real_text_list = [item.text for item in res]
