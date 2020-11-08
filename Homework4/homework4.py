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

def show(im_list, quality_type, quality):
	""" Show input (filtered image) compared to the original
    gray scale image """
	pyplot.figure(figsize=(12,8))
	i = 1
	original = im_list[0]
	qual1 = float(quality.pop(0))
	pyplot.subplot(2, 4, 1)
	pyplot.title(f"{original[1]}\n{quality_type}: {qual1:.4f}")
	pyplot.imshow(original[0], cmap="gray")
	for im in im_list[1 - len(im_list):]:
		qual = float(quality.pop(0))
		pyplot.subplot(2, 4, 4 + i)
		pyplot.title(f"{im[1]}\n{quality_type}: {qual:.4f}")
		pyplot.imshow(im[0], cmap='gray')
		i += 1
	pyplot.show()

def gaussian_noise(image):
	""" Creates a gaussian noise corruption of image """
	l, w = image[0].shape[:2]
	sigma = 10
	noise = sigma * numpy.random.randn(l, w)
	return image[0] + noise

def salt_pepper_noise(image):
	""" Creates a salt and pepper noise corruption of image """
	l, w = image[0].shape[:2]
	salt_and_pepper = numpy.ones((l, w))
	for i in range(l):
		for j in range(w):
			pixel = random.randint(0, 15)
			if (pixel == 0):
				salt_and_pepper[i][j] = pixel
			elif (pixel == 1):
				salt_and_pepper[i][j] = 255
			else:
				salt_and_pepper[i][j] = image[0][i][j]
	return salt_and_pepper

def contrast_stretch(image):
	""" Creates a contrast stretch enhancement of image """
	pixel_max = numpy.amax(image[0])
	pixel_min = numpy.amin(image[0])
	return (image[0] - pixel_min) / (pixel_max - pixel_min) * 255

def gamma_correction(image):
	""" Creates a contrast stretch enhancement of image """
	l, w = image[0].shape[:2]
	pixel_max = numpy.amax(image[0])
	pixel_min = numpy.amin(image[0])
	gamma = numpy.zeros((l, w))
	image_binary = image[0] / 255
	gamma = image_binary ** 1.8
	return gamma

def quality_by_PSNR(original, altered):
	for a in altered:
		mean_square = numpy.mean((original[0] - a[0]) ** 2)
		if (mean_square == 0):
			yield('inf')
		else :
			yield str(20 * math.log10(255 / math.sqrt(mean_square)))


def quality_by_MSE(original, altered):
	for a in altered:
		ori = original[0].astype(numpy.float64)
		alt = a[0].astype(numpy.float64)
		yield numpy.mean((ori - alt) ** 2)

def quality_by_SSIM(original, altered):
	C1 = 6.5025
	C2 = 58.5225
	
	original = original[0].astype(numpy.float64)
	altered = altered[0].astype(numpy.float64)
	kernel = cv2.getGaussianKernel(11, 1.5)
	window = numpy.outer(kernel, kernel.transpose())
	
	mu_ori = cv2.filter2D(original, -1, window)[5:-5, 5:-5]     
	mu_alt = cv2.filter2D(altered, -1, window)[5:-5, 5:-5]
	mu_ori_sq = mu_ori ** 2
	mu_alt_sq = mu_alt ** 2
	mu_dif = mu_ori * mu_alt
	
	sigma_ori_sq = cv2.filter2D(original ** 2, -1, window)[5:-5, 5:-5]
	sigma_alt_sq = cv2.filter2D(altered ** 2, -1, window)[5:-5, 5:-5]
	sigma_dif = cv2.filter2D(original * altered, -1, window)[5:-5, 5:-5]

	sigma_ori_sq = sigma_ori_sq - mu_ori_sq
	sigma_alt_sq = sigma_alt_sq - mu_alt_sq
	sigma_dif = sigma_dif - mu_dif	

	ssim_map = ((2 * mu_dif + C1) * (2 * sigma_dif + C2)) / \
		((mu_ori_sq + mu_alt_sq + C1) * (sigma_ori_sq + sigma_alt_sq + C2))

	return ssim_map.mean()

def generator_to_list(gen):
	l = []
	for i in gen:
		l.append(i)
	return l

def get_original(file_name):
	""" Acquire and adjust the original image """
	original = cv2.imread(file_name)
	original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
	return original


if __name__ == "__main__":
	image_file = "lena_g.bmp"
	images = []

	images.append((get_original(image_file), "Original"))
	images.append((gaussian_noise(images[0]), "Gaussian"))
	images.append((salt_pepper_noise(images[0]), "Salt and Pepper"))
	images.append((contrast_stretch(images[0]), "Contrast Stretch"))
	images.append((gamma_correction(images[0]), "Gamma Correction"))

	psnr = quality_by_PSNR(images[0], images)
	mse = quality_by_MSE(images[0], images)
	ssim = []

	psnr = generator_to_list(psnr)
	mse = generator_to_list(mse)
	for i in images:
		ssim.append(quality_by_SSIM(images[0], i))

	show(images, "PSNR", psnr)
	show(images, "MSE", mse)
	show(images, "SSIM", ssim)
