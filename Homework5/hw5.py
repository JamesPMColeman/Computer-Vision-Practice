#=============================================================================#
#                                                                             #
#           James Coleman                                                     #
#           CS 3150                                                           #
#           Homework 5: Saliency                                              #
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
from matplotlib import pyplot

def show(im_list, title, quality):
    """ Show input (filtered image) compared to the original
    gray scale image """
    pyplot.figure(figsize=(10,7))
    for i in range(1, len(im_list) + 1):
        pyplot.subplot(2, 3, i)
        pyplot.title(f"{title[i - 1]}\n{quality[i - 1]:.4f}")
        pyplot.imshow(im_list[i - 1], cmap="gray")
    pyplot.show()

def show_one(im):
    pyplot.imshow(im, cmap="gray")
    pyplot.show()

def gaussian_noise(image, salience_map, threshold):
    """ Creates a gaussian noise corruption of image """
    l, w = image.shape[:2]
    new_image = numpy.zeros((l, w))
    sigma = 10
    noise = sigma * numpy.random.randn(l, w)
    for i in range(l):
        for j in range(w):
            if threshold(salience_map[i][j]):
                new_image[i][j] = image[i][j] + noise[i][j]
            else:
                new_image[i][j] = image[i][j]
    return new_image

def quality_MSE(original, altered):
    ori = original.astype(numpy.float64)
    alt = altered.astype(numpy.float64)
    return numpy.mean((ori - alt) ** 2)

def salience_MSE(original, altered, salience_map):
    l, w = original.shape[:2]
    diff = numpy.zeros((l, w))
    
    ori = original.astype(numpy.float64)
    alt = altered.astype(numpy.float64)
    for i in range(l):
        for j in range(w):
            if salience_map[i][j] >= .08:
                diff[i][j] = ori[i][j] - alt[i][j]
            else:
                diff[i][j] = 0
        
    return numpy.mean(diff ** 2)

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
    image_titles = [
        "Original",
        "Saliency Map",
        "Uniform Gaussian Noise",
        "Consequential Noise",
        "Inconsequential Noise",
    ]

    for i in image_list:
        images = []
        mse_qualities = []
        mse_plus_saliency = []
        images.append(get_original(i))
        images.append(saliency(images[0]))
        images.append(gaussian_noise(images[0], \
                                     images[1], \
                                     lambda i=i: True))
        images.append(gaussian_noise(images[0], \
                                     images[1], \
                                     lambda i=i: i >= 0.1))
        images.append(gaussian_noise(images[0], \
                                     images[1], \
                                     lambda i=i: i <= 0.1))
        for im in images:
            mse_qualities.append(quality_MSE(images[0], im))
        show(images, image_titles, mse_qualities)

        for im in images:
            mse_plus_saliency.append(salience_MSE(images[0], im, images[1]))
        show(images, image_titles, mse_plus_saliency)
