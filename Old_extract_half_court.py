#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 18:42:54 2018

@author: jinzhao
"""
import numpy as np
import cv2
import copy
import scipy.ndimage

def binarize_image(image, threshold):
    m, n = image.shape
    result = np.zeros((m, n)).astype('uint8')
    for i in range(m):
        for j in range(n):
            if image[i, j] >= threshold:
                result[i, j] = 255
    
    return result
 
# Main
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
if __name__ == "__main__":
    img = cv2.imread('shotchart_orig.png') 
    img_blue = img[:, :, 0]
    img_ = img_blue[30:500, 12:508]
    img_bw = binarize_image(img_, 210)
    
    cv2.imwrite('half_court.png', img_bw)
    
    cv2.imshow('test0', img_bw)
    cv2.waitKey(1)
    cv2.destroyAllWindows() 


