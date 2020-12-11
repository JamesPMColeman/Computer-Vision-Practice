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
wall = cv2.imread('./test4.jpg')
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
green_high = (160, 210, 120)
green_low = (80, 130, 30)
yellow_high = (255, 255, 75)
yellow_low = (155, 120, 0)
orange_high = (255, 90, 75)
orange_low = (115, 50, 30)
pink_high = (255, 95, 160)
pink_low = (160, 40, 70)
blue_high = (100, 155, 255)
blue_low = (25, 45, 120)
purple_high = (140, 70, 120)
purple_low = (75, 40, 60)

## yellow_swatche = numpy.full((10, 10, 3), yellow_high, dtype=numpy.uint8)
## gray_swatche = numpy.full((10, 10, 3), yellow_low, dtype=numpy.uint8)
## show(yellow_swatche, "RGB")
## show(gray_swatche, "RGB")

green_mask = cv2.inRange(wall, green_low, green_high)
green_holds = cv2.bitwise_and(wall, wall, mask=green_mask)
yellow_mask = cv2.inRange(wall, yellow_low, yellow_high)
yellow_holds = cv2.bitwise_and(wall, wall, mask=yellow_mask)
orange_mask = cv2.inRange(wall, orange_low, orange_high)
orange_holds = cv2.bitwise_and(wall, wall, mask=orange_mask)
pink_mask = cv2.inRange(wall, pink_low, pink_high)
pink_holds = cv2.bitwise_and(wall, wall, mask=pink_mask)
blue_mask = cv2.inRange(wall, blue_low, blue_high)
blue_holds = cv2.bitwise_and(wall, wall, mask=blue_mask)
purple_mask = cv2.inRange(wall, purple_low, purple_high)
purple_holds = cv2.bitwise_and(wall, wall, mask=purple_mask)

show(blue_mask, "gray")
show(blue_holds, "RGB")

# circle routes of a particular color

# connect route as a graph
