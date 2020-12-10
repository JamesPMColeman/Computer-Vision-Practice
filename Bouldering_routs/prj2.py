#=============================================================================#
#                                                                             #
#           James Coleman                                                     #
#           CS 3150                                                           #
#           Project 2: Identify Bouldering Routes                             #
#           November 13th, 2020                                               #
#                                                                             #
#                                                                             #
#=============================================================================#

        #
        #    >>>>>>>>>>>>>>> Goals <<<<<<<<<<<<<<<<
        #
        #       
        #
        #
        #

# imports
import cv2
import numpy
from matplotlib import cm
from matplotlib import pyplot
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D

# helper functions
def max_of_three(i, j, k): 
    """ returns the max of three """
    mot = i if (i > j) else j
    return mot if (mot > k) else k

def show(image, color):
	""" Helper method to display a single image 
	with pyplot """
	if (color == "gray"):
		pyplot.imshow(image, cmap="gray")
	else:
		pyplot.imshow(image)
	pyplot.show()

def plot(image, c1, c2, c3, x, y, z):
	p = pyplot.figure()
	pixels = image.reshape((numpy.shape(image)[0] * numpy.shape(image)[1], 3))
	normal = colors.Normalize(vmin=-1.,vmax=1.)
	normal.autoscale(pixels)
	pixels = normal(pixels).tolist()
	axis = p.add_subplot(1, 1, 1, projection="3d")
	axis.scatter(c1.flatten(), c2.flatten(), c3.flatten(), \
				 c=pixels, marker=".")
	axis.set_xlabel(x)
	axis.set_ylabel(y)
	axis.set_zlabel(z)
	pyplot.show()
	

# read input image
wall = cv2.imread('./hold1.png')
## show(wall)
length, width, depth = wall.shape

# Convert color from BGR to RGB
wall = cv2.cvtColor(wall, cv2.COLOR_BGR2RGB)
show(wall, "RGB")

# make black and white version
wall_gray = cv2.cvtColor(wall, cv2.COLOR_RGB2GRAY)
## show(wall_gray, "gray")

# make scatter plots of colors
wall_hsv = cv2.cvtColor(wall, cv2.COLOR_RGB2HSV)
red, green, blue = cv2.split(wall)
hue, sat, val = cv2.split(wall_hsv)

## plot(wall, red, green, blue, "Red", "Green", "Blue")
## plot(wall_hsv, hue, sat, val, "Hue", "Saturation", "Value")


# use saliency to identify holds
##s = cv2.saliency.StaticSaliencySpectralResidual_create()
##worked, saliency_wall = s.computeSaliency(wall_gray)
##show(saliency_wall, "gray")

# use color mask to isolate holds
yellow = (255, 219, 41)
gray_yellow = (220, 170, 0)

## yellow_swatche = numpy.full((10, 10, 3), yellow, dtype=numpy.uint8)
## gray_swatche = numpy.full((10, 10, 3), gray_yellow, dtype=numpy.uint8)
## show(yellow_swatche, "RGB")
## show(gray_swatche, "RGB")

yellow_mask = cv2.inRange(wall, gray_yellow, yellow)
yellow_holds = cv2.bitwise_and(wall, wall, mask=yellow_mask)

pyplot.subplot(1, 2, 1)
pyplot.imshow(yellow_mask, cmap="gray")
pyplot.subplot(1, 2, 2)
pyplot.imshow(yellow_holds)
pyplot.show()

show(yellow_mask, "gray")
show(yellow_holds, "RGB")

# circle routes of a particular color

# connect route as a graph
