#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 13:42:42 2018

@author: jinzhao
"""
import cv2
import numpy as np
import scipy.ndimage

def extract_spots(img, threshold):
    m, n = img.shape
    result = np.zeros((m, n)).astype('uint8')
    
    for i in range(m):
        for j in range(n):
            if img[i, j] < threshold:
                result[i, j] = 255
                
    return result

def generate_disk_filter(radius):
    
    L = np.arange(-radius, radius + 1)
    X, Y = np.meshgrid(L, L)
    disk = np.array((X ** 2 + Y ** 2) <= radius ** 2, dtype = 'uint8')
    
    return disk

def process_made_shot(shot_made):
    img_filled = scipy.ndimage.binary_fill_holes(shot_made).astype('uint8')
    img_filled[img_filled == 1] = 255
    img_diff = img_filled - shot_made

    disk_filter_1 = generate_disk_filter(1)
    disk_filter_2 = generate_disk_filter(1)
    temp = cv2.erode(img_diff, disk_filter_1, iterations = 1)
    made_shots = cv2.dilate(temp, disk_filter_2, iterations = 1)
    
    return made_shots

def process_missed_shot(shot_missed):
    
    square_filter_1 = np.ones((4, 4))
    temp = cv2.erode(shot_missed, square_filter_1, iterations = 1)
    square_filter_2 = np.ones((2, 2))
    missed_shots = cv2.dilate(temp, square_filter_2, iterations = 1)
    
    return missed_shots

def calculate_shot_pos(contours):
    
    n_spots = len(contours)
    moments = np.empty((0, 2))
    
    for i in range(n_spots):
        cnt = contours[i]
        M = cv2.moments(cnt)
        col_ind = int(M['m10']/M['m00'])
        row_ind = int(M['m01']/M['m00'])  
        centroid = np.array([row_ind, col_ind])
        moments = np.vstack((moments, centroid))
    
    return moments


def extract_shot_information(img_file):
    img_brg = cv2.imread(img_file) # Blue-Red-Green
    shot_chart = img_brg[30:500, 12:508]
    height, width, depth = shot_chart.shape
    
    green_channel = shot_chart[:, :, 2]
    red_channel = shot_chart[:, :, 1]
    
    threshold = 100
    
    img_missed_shots = extract_spots(red_channel, threshold)
    img_missed_shots[445:460, :] = 0
    missed_shots = process_missed_shot(img_missed_shots)

    img_made_shots = extract_spots(green_channel, threshold)
    img_made_shots[445:460, :] = 0
    made_shots = process_made_shot(img_made_shots)
    
    im1, contours_1, hierarchy1 = cv2.findContours(made_shots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    im2, contours_2, hierarchy2 = cv2.findContours(missed_shots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    made_shots_pos = calculate_shot_pos(contours_1)
    missed_shots_pos = calculate_shot_pos(contours_2)
    
    return made_shots_pos, missed_shots_pos

if __name__ == "__main__":
    file = "shotchart.png"
    
    made_shots_pos, missed_shots_pos = extract_shot_information(file)
    
    img = cv2.imread(file)[30:500, 12:508][:, :, 1] # Blue-Red-Green
    img = extract_spots(img, 100)
    cv2.imshow('test1', img)
    cv2.waitKey(1)
    cv2.destroyAllWindows() 
    
