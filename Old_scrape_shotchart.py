#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 00:16:37 2018

@author: jinzhao
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import cv2
import requests
from PIL import Image
import numpy as np

# Scrape
url = "https://www.basketball-reference.com/boxscores/shot-chart/201805310GSW.html"
html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")

image_links = []
for link in soup.find_all('img'):
    image_links.append(link.get("src"))

img_url = image_links[3]
im = Image.open(urlopen(img_url))
img = np.array(im)

cv2.imshow('test1', img)
cv2.waitKey(1)
cv2.destroyAllWindows() 



