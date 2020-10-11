#===============================================================#
#                                                               #
#   James Coleman                                               #
#   CS 3150                                                     #
#   Homework 2 part one                                         #
#   September 15th                                              #
#                                                               #
#===============================================================#

    #          >>>>>>>>>> Goals <<<<<<<<<<
    #
    #   1. Detect skin in normal and low light images
    #   2. Remove the background of the low light image
    #   before doing skin detection
    #   3. Display results
    #
    #
    #

# Imports
import numpy
import cv2
from matplotlib import pyplot

# Helper methods
def show(image, title):
    """ Helper method to display a single image 
    with pyplot """
    pyplot.figure()
    pyplot.title(title)
    pyplot.imshow(image)
    pyplot.show()

# List out all cv2 color conversions
## This is based on code from Rebecca Stone's article 'Image
## Segmentation Using Color Spaces in OpenCV + Python' on 
## realpython.com
transformations = [i for i in dir(cv2) if i.startswith('COLOR_')]
for i in transformations:
	pass ## print(i)

# Read in the images, convert them to RGB and display
nrm = cv2.imread('face_good.bmp')
low = cv2.imread('face_dark.bmp')

normal_light = cv2.cvtColor(nrm, cv2.COLOR_BGR2RGB)
low_light    = cv2.cvtColor(low, cv2.COLOR_BGR2RGB)

show(normal_light, "Normal Light")
show(low_light, "Low Light")

# Use a color mask to isolate skin in normal light image
blue  = nrm[:,:,0].astype(numpy.int16)
green = nrm[:,:,1].astype(numpy.int16) 
red   = nrm[:,:,2].astype(numpy.int16)

mask = (red > 96) & (green > 40) & (blue > 10) &                \
	   ((nrm.max() - nrm.min()) > 15) & 	    \
	   (numpy.abs(red - green) > 15) &							\
	   (red > green) &											\
	   (red > blue) 

skin_nrm = nrm * mask.reshape(mask.shape[0], mask.shape[1], 1)
skin_normal_light = cv2.cvtColor(skin_nrm, cv2.COLOR_BGR2RGB)

show(skin_normal_light, "Normal light skin detection")

# Convert low light image to Lumens image, remove background
lumens = cv2.cvtColor(low, cv2.COLOR_BGR2LUV)
length, width, depth = lumens.shape
show(lumens, "Low-light image in Lumens")

## Create a histogram of the lumens and use a mask to detect a
## threshold
histogram = numpy.zeros(256)

for i in range(length):
	for j in range(width):
		lum = low[i,j,0] * .299 +								\
			  low[i,j,1] * .587 +								\
			  low[i,j,2] * .114
		histogram[int(lum)] = histogram[int(lum)] + 1 

trough_detection = ([
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, -2, -2, -2, -2, -2,
	-2, -2, -2, -2, -2, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
	])

trough = numpy.convolve(histogram, trough_detection, mode='same')
thresh = trough.argmax()
pyplot.plot(histogram)
pyplot.show()
pyplot.plot(trough)
pyplot.show()

# Use lumens image as a mask on lowlight image
for i in range(length):
	for j in range(width):
		if (low[i,j,0] * .299 +								\
			low[i,j,1] * .587 +								\
			low[i,j,2] * .114 > thresh): 
			low[i,j,0] = 0
			low[i,j,1] = 0
			low[i,j,2] = 0
		
show(low, "Low-light after threshold mask")

# Isolate skin of low light image

blue  = low[:,:,0].astype(numpy.int16)
green = low[:,:,1].astype(numpy.int16) 
red   = low[:,:,2].astype(numpy.int16)

mask = (red > 96) & (green > 40) & (blue > 10) &                \
	   ((low.max() - low.min()) > 15) & 	    \
	   (numpy.abs(red - green) > 15) &							\
	   (red > green) &											\
	   (red > blue) 

skin_low = low * mask.reshape(mask.shape[0], mask.shape[1], 1)
skin_low_light = cv2.cvtColor(skin_low, cv2.COLOR_BGR2RGB)

show(skin_low_light, "Low-light skin detection")
