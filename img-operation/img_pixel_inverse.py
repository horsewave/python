""" run a batch of ggems using python

@file change_batch_file_names.py
@detail :write your Description
@author Bo Ma
@date 2019.09.28
Email:mabo@ihep.ac.cn
Tel:010-88235869
Cell:15210606357
@version 1.0
"""

import subprocess
import time

import cv2
# opencv读取图像
img = cv2.imread('/home/mabo/Pictures/my-pic.png', 1)
cv2.imshow('img', img)
img_shape = img.shape  # 图像大小(565, 650, 3)

print(img_shape)
h = img_shape[0]
w = img_shape[1]
# 彩色图像转换为灰度图像（3通道变为1通道）
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(gray.shape)
# 最大图像灰度值减去原图像，即可得到反转的图像
dst = 255 - gray
cv2.imshow('dst', dst)
#  cv2.waitKey(0)

cv2.imwrite('/home/mabo/Pictures/my-pic_inverse.png',dst)
print('Successfully saved')
