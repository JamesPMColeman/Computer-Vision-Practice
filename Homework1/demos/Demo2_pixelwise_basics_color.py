#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 12:08:39 2020

"""
#https://note.nkmk.me/en/python-opencv-bgr-rgb-cvtcolor/#:~:text=When%20the%20image%20file%20is,to%20convert%20BGR%20and%20RGB.

import numpy as np
import cv2 
import math
import random
from matplotlib import pyplot as plt
#from google.colab.patches import cv2_imshow

#test image 1  
im=cv2.imread('./1_test.jpg')
#im_rgb = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
length, width = img.shape
radius = 0.45*min(length,width)
for i in range(length):     # this is the row
    for j in range(width):  # this is the column      
        if math.sqrt((i-length/2)**2 + (j-width/2)**2) > radius:
             img[i,j] = 0       
plt.figure()
plt.imshow(img,cmap='gray', vmin=0, vmax=255)  

 


#what will happen if I don't change back to BGR and show it?        
#windowname = 'image'
#cv2.imshow(windowname,imrgb) #this should work but not in Colab
#cv2.waitKey()  
#cv2.destroyAllWindows() 