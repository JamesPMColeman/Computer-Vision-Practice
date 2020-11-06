#=============================================================================#
#																			  #
#			James Coleman													  #
#			CS 3150															  #
#			Homework 4														  #
#			November 6th, 2020												  #
#																			  #
#=============================================================================#

		#
		#		>>>>>>>>>>>>>>>>>>> Goals <<<<<<<<<<<<<<<<<<<<<
		#
		#	1. Create two corrupted versions of the Lena image
		#	2. Create two enhanced versions of the Lena image
		#	3. Measure each image's quality by PSNR, MSE and SSIM
		#
		#
		#

# Imports
import cv2
import numpy
from random import Random
from matplotlib import pyplot

def show(image, title):
	""" Helper method to display a single image 
    with pyplot """
	pyplot.figure()
	pyplot.title(title)
	pyplot.imshow(image)
	pyplot.show()

def gaussian_noise(image):
	pass

def salt_pepper_noise(image):
	pass

def contrast_stretch(image):
	pass

def gamma_correction(image):
	pass

def get_original(file_name):
	""" Acquire and adjust the original image """
	original = cv2.imread(file_name)
	return original


if __name__ == "__main__":
	image_file = "lena_g.bmp"
	original = get_original(image_file)
	show(original, "Original")
