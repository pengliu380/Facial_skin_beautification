# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 17:07:00 2018

@author: liupeng
"""

import cv2 as cv
import numpy as np

def nothing(x):
    pass
def custom_blur(image):
    kernel = np.array([[0, -1, 0], [-1, 4.9, -1], [0, -1, 0]], np.float32) #锐化
    dst = cv.filter2D(image, -1, kernel=kernel)
    return dst 
    
img = cv.imread('man.jpg')
cv.namedWindow('image',cv.WINDOW_NORMAL)
#cv.namedWindow('image')
# 创建两个滑块
cv.createTrackbar('space_parameter', 'image', 0, 100, nothing)
cv.createTrackbar('range_parameter', 'image', 0, 100, nothing)
cv.createTrackbar('brightness', 'image', 0, 100, nothing)
cv.createTrackbar('contrast', 'image', 100, 300, nothing)
cv.createTrackbar('custom', 'image', 0, 1, nothing)

temp = img.copy()

while(True):
    tmp = np.hstack((img, temp))
    cv.imshow('image',tmp)
    if cv.waitKey(1) == 27:
        break
    if cv.waitKey(1) == ord('s'):
        cv.imwrite('beautiful_image.png',temp)
        break
    # 得到四个滑块的值
    sigma_s = cv.getTrackbarPos('space_parameter', 'image')
    sigma_r = cv.getTrackbarPos('range_parameter', 'image')
    brightness = cv.getTrackbarPos('brightness', 'image')
    contrast = cv.getTrackbarPos('contrast', 'image') * 0.01
    custom = cv.getTrackbarPos('custom', 'image')
    # 双边滤波
    temp = cv.bilateralFilter(img, 15, sigma_r, sigma_s)
    # 进行对比度和亮度调整
    temp = np.uint8(np.clip(contrast * temp + brightness, 0, 255))
    # 锐化
    if custom == 1:
        temp = custom_blur(temp)