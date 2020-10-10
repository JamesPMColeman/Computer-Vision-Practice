#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 09:24:52 2020
 
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def luv_space_gamma( src, gamma ):
    luv = cv.cvtColor(src, cv.COLOR_BGR2LUV)
    #// extract luminance channel
    l = luv[:,:,0]
    #// normalize 
    l = l / 255.0
    #// apply power transform
    l = np.power(l, gamma)
    #// scale back
    l = l * 255
    luv[:,:,0] = l.astype(np.uint8)
    rgb = cv.cvtColor(luv, cv.COLOR_LUV2BGR)
    return rgb

def skin_rgb_threshold( src ):
    # extract color channels and save as SIGNED ints
    # need the extra width to do subraction
    b = src[:,:,0].astype(np.int16)
    g = src[:,:,1].astype(np.int16)
    r = src[:,:,2].astype(np.int16)

    skin_mask =                                    \
          (r > 96) & (g > 40) & (b > 10)           \
        & ((src.max() - src.min()) > 15)           \
        & (np.abs(r-g) > 15) & (r > g) & (r > b)    

    return src * skin_mask.reshape(skin_mask.shape[0], skin_mask.shape[1], 1)

def find_local_min( hist ):

    kern = np.array(
            [2,0,0,0,
             2,0,0,0,
             2,0,0,0,
             2,0,0,0,
             1,0,0,0,
             1,0,0,0,
             1,0,0,0,
             1,0,0,0,
             -3,-3,-3,-3
             -3,-3,-3,-3
             ,0,0,0,1
             ,0,0,0,1
             ,0,0,0,1
             ,0,0,0,1
             ,0,0,0,2
             ,0,0,0,2
             ,0,0,0,2
             ,0,0,0,2])
    #// theres a lot of 0's in there what will throw off 
    #// the convolution
    hist[0] = 0
    deriv = np.convolve(hist, kern, mode='same')
    threshold = deriv.argmax()
    return threshold, deriv


###########################################################################
#                          MAIN CODE STARTS HERE                          #
###########################################################################
#//load up the images and do gamma correction in LUV then show the results
    
src1 = cv.imread("face_good.bmp", cv.IMREAD_COLOR)
plt.figure()
plt.title('good face')
plt.imshow(cv.cvtColor(src1,cv.COLOR_BGR2RGB) ) 
# detect the skin after gamma 
#rgb = cv.cvtColor(luv, cv.COLOR_LUV2BGR)
skin = skin_rgb_threshold(src1)
plt.figure()
plt.title('skin1 detected')
plt.imshow(cv.cvtColor(skin,cv.COLOR_BGR2RGB))

src = cv.imread("face_dark.bmp", cv.IMREAD_COLOR)
plt.figure()
plt.title('BGR imread from opencv')
plt.imshow(src ) 
#gamma = luv_space_gamma(src, 0.6)
luv = cv.cvtColor(src, cv.COLOR_BGR2Luv)
#// extract luminance channel
l = luv[:,:,0]
#// normalize 
l = l / 256.0
##// apply power transform#
l = l**0.6 #np.power(l, 0.6)   #gamma =0.6
##// scale back
l = l * 256
luv[:,:,0] =l  #.astype(np.uint8)
gamma = cv.cvtColor(luv, cv.COLOR_LUV2BGR)
##cv.imwrite("face_gamma.jpg", gamma)
#
plt.figure()
plt.title('rgb')
plt.imshow(cv.cvtColor(src,cv.COLOR_BGR2RGB)) 

plt.figure()
plt.title('rgb face_gama 0.6')
plt.imshow(cv.cvtColor(gamma,cv.COLOR_BGR2RGB)) 

# detect the skin after gamma 
rgb = cv.cvtColor(luv, cv.COLOR_LUV2BGR)
skin = skin_rgb_threshold(rgb)
plt.figure()
plt.title('skin detected')
plt.imshow(cv.cvtColor(skin,cv.COLOR_BGR2RGB))