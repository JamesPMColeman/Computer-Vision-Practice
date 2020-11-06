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
	pyplot.imshow(image, cmap="gray")
	pyplot.show()

def gaussian_noise(image):
	""" Creates a gaussian noise corruption of image """
	l, w = image.shape[:2]
	sigma = 10
	noise = sigma * numpy.random.randn(l, w)
	return image + noise

def salt_pepper_noise(image):
	pass

def contrast_stretch(image):
	pass

def gamma_correction(image):
	pass

def get_original(file_name):
	""" Acquire and adjust the original image """
	original = cv2.imread(file_name)
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	return original


if __name__ == "__main__":
	image_file = "lena_g.bmp"
	original = get_original(image_file)
	gaussian = gaussian_noise(original)
	show(original, "Original")
	show(gaussian, "Gaussian")
