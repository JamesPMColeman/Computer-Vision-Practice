#=============================================================================#
#																			  #
#			James Coleman													  #
#			CS 3150															  #
#			Homework 5: Saliency											  #
#			November 13th, 2020												  #
#																			  #
#																			  #
#=============================================================================#

		#
		# 	 >>>>>>>>>>>>>>> Goals <<<<<<<<<<<<<<<<
		#
		#		
		#
		#
		#

# imports
import cv2
import numpy
from matplotlib import pyplot

def show(im_list, quality_type, quality):
    """ Show input (filtered image) compared to the original
    gray scale image """
    pyplot.figure(figsize=(12,8))
    for i in range(1, len(im_list) + 1):
        pyplot.subplot(1, len(im_list), i)
        pyplot.title(f"{quality[i - 1]}\n{quality_type}")
        pyplot.imshow(im_list[i - 1], cmap="gray")
    pyplot.show()

def gaussian_noise(image):
    """ Creates a gaussian noise corruption of image """
    l, w = image.shape[:2]
    sigma = 10
    noise = sigma * numpy.random.randn(l, w)
    return image + noise

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
    mu_product = mu_ori * mu_alt

    sigma_ori_sq = cv2.filter2D(original ** 2, -1, window)[5:-5, 5:-5]
    sigma_alt_sq = cv2.filter2D(altered ** 2, -1, window)[5:-5, 5:-5]
    sigma_product = cv2.filter2D(original * altered, -1, window)[5:-5, 5:-5]

    sigma_ori_sq = sigma_ori_sq - mu_ori_sq
    sigma_alt_sq = sigma_alt_sq - mu_alt_sq
    sigma_product = sigma_product - mu_product

    ssim_map = ((2 * mu_product + C1) * (2 * sigma_product + C2)) / \
        ((mu_ori_sq + mu_alt_sq + C1) * (sigma_ori_sq + sigma_alt_sq + C2))

    return ssim_map.mean()

def saliency(image):
	s = cv2.saliency.StaticSaliencySpectralResidual_create()
	worked, saliency_image = s.computeSaliency(image)

	return saliency_image

def get_original(file_name):
    """ Acquire and adjust the original image """
    original = cv2.imread(file_name)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    return original


if __name__ == "__main__":
	image_list = [
		"Saliency0.jpg",
		"Saliency1.jpeg",
		"Saliency2.jpg",
		"Saliency3.png",
		"Saliency4.png",
	]

	for i in image_list:
		images = []
		qualities = []
		images.append(get_original(i))
		images.append(saliency(images[0]))
		print(images[1].max())
		images.append(gaussian_noise(images[0]))
		qualities = list(quality_by_MSE(images[0], images))
		
		show(images, "n", qualities)
	

	

