#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 12:08:39 2020

"""

import numpy as np
import cv2 
import math
import random
from matplotlib import pyplot as plt
#from google.colab.patches import cv2_imshow

#test image matrix  
im1 = np.zeros((200,200))
length, width = im1.shape
for i in range(length):     # this is the row
    for j in range(width):  # this is the column
        im1[i,j] = j        # try i as well       
                      
print(im1[0,0])          
print(im1[0,199])  #last column, first row
print(im1[199,0])  #last row   
plt.subplot(2,2,1)
plt.imshow(im1,cmap='gray', vmin=0, vmax=255)     
      
#test image matrix 2
im1 = np.zeros((200,200))
length, width = im1.shape
for i in range(length):     # this is the row
    for j in range(width):  # this is the column
        #im1[i,j] = random.random()*255  
        im1[i,j] = random.randint(0, 1)*255
plt.subplot(2,2,2)                                                
plt.imshow(im1,cmap='gray', vmin=0, vmax=255) 


#test image matrix 3
im1 = np.zeros((200,200))        
im1[100:110,:]=255
im1[:,100:110]=255  
plt.subplot(2,2,3)
plt.imshow(im1,cmap='gray', vmin=0, vmax=255) 


#test image matrix  n
im1 = np.zeros((200,200))
length, width = im1.shape
radius = 0.5*min(length,width)

for i in range(length):     # this is the row
    for j in range(width):  # this is the column      
        if math.sqrt((i-length/2)**2 + (j-width/2)**2) > radius:
             im1[i,j] = 255       
            
plt.subplot(2,2,4)
plt.imshow(im1,cmap='gray', vmin=0, vmax=255)
plt.show()
#windowname = 'image'
#cv2.imshow(windowname,im1) #this should work but not in Colab
            
 



#cv2.imshow(windowname,im1) 
#cv2.waitKey()  
#cv2.destroyAllWindows() 
