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
	#	1. Detect skin in normal and low light images
	#	2. Remove the background of the low light image
	#	before doing skin detection
	#	3. Display results
	#
	#
	#

# Imports

# Helper methods
# Read in the images, convert them to RGB and display
# Use a color mask to isolate skin in normal light image
# Convert low light image to Lumens image, remove background
# Use lumens image as a mask on lowlight image
# Isolate skin of low light image
