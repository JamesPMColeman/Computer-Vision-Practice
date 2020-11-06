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
import math
import numpy
import random
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
	""" Creates a salt and pepper noise corruption of image """
	l, w = image.shape[:2]
	salt_and_pepper = numpy.ones((l, w))
	for i in range(l):
		for j in range(w):
			pixel = random.randint(0, 15)
			if (pixel == 0):
				salt_and_pepper[i][j] = pixel
			elif (pixel == 1):
				salt_and_pepper[i][j] = 255
			else:
				salt_and_pepper[i][j] = image[i][j]
	return salt_and_pepper

def contrast_stretch(image):
	""" Creates a contrast stretch enhancement of image """
	pixel_max = numpy.amax(image)
	pixel_min = numpy.amin(image)
	return (image - pixel_min) / (pixel_max - pixel_min) * 255

def gamma_correction(image):
	""" Creates a contrast stretch enhancement of image """
	l, w = image.shape[:2]
	pixel_max = numpy.amax(image)
	pixel_min = numpy.amin(image)
	gamma = numpy.zeros((l, w))
	image_binary = image / 255
	gamma = image_binary ** 1.8
	return gamma

def quality_by_PSNR(original, altered):
	mean_square = numpy.mean((original, altered))
	if (mean_square == 0): 
		return('inf')
	return str(20 * math.log10(255 / math.sqrt(mean_square)))

def quality_by_MSE(original, altered):
	pass

def quality_by_SSIM(original, altered):
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
	salt_pep = salt_pepper_noise(original)
	contrast = contrast_stretch(original)
	gamma_im = gamma_correction(original)

	psnr = quality_by_PSNR(original, gaussian)

	show(original, "Original")
	show(gaussian, "Gaussian")
	show(salt_pep, "Salt and Pepper")
	show(contrast, "Contrast stretch")
	show(gamma_im, "Gamma correction")
