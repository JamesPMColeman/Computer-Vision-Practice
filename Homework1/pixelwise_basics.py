#!/usr/bin/env python3

import numpy as np
import cv2
import math
import random
from matplotlib import pyplot as plt

# test image matrix
im1 = np.zeros((200, 200))
length, width = im1.shape

print(width)
print(length)

for i in range(length):
	for j in range(width):
		im1[i,j] = j
		#print("Pixel " + str(i) + ", " + str(j) + ": " + str(im1[i,j]))

print(im1[0,0])
print(im1[0,199])
print(im1[199,0])
#plt.figure()
#plt.imshow(im1, cmap='gray', vmin=0, vmax=255)

cv2.imshow('Image one', im1)
cv2.waitKey()
cv2.destroyAllWindows()
