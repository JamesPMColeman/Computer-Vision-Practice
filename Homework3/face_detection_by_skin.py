#===============================================================#
#                                                               #
#   James Coleman                                               #
#   CS 3150                                                     #
#   Homework 2 part one                                         #
#   September 15th                                              #
#                                                               #
#===============================================================#

    #              >>>>>>>>>> Goals <<<<<<<<<<
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

# Read in the images, convert them to RGB and display
normal_light = cv2.imread('face_good.bmp')
low_light    = cv2.imread('face_dark.bmp')

normal_light = cv2.cvtColor(normal_light, cv2.COLOR_BGR2RGB)
low_light    = cv2.cvtColor(low_light, cv2.COLOR_BGR2RGB)

show(normal_light, "Normal Light")
show(low_light, "Low Light")

# Use a color mask to isolate skin in normal light image
# Convert low light image to Lumens image, remove background
# Use lumens image as a mask on lowlight image
# Isolate skin of low light image
