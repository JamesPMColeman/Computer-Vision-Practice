#===============================================================#
#																#
# 	James Coleman												#
#	CS 3150														#
#	Homework 2 part one											#
#	September 15th												#
#																#
#===============================================================#

	#	           >>>>>>>>>> Goals <<<<<<<<<<
	#
	#  1. Apply Averaging, Sobel, Laplacian, Median and 
	#     Gaussian filters to my image
	#  2. Apply two other filters of my choice
	#  3. Analyze the different filter effects 
	#
	#

# Imports 
import cv2
import numpy
from random import randrange
from matplotlib import pyplot

# Helper methods
   # Show images
def show(im_list):
	''' Show input (filtered image) compared to the original
	gray scale image '''
	pyplot.figure(figsize=(12,6))
	i = 1
	pyplot.subplot(1, len(im_list) + 1, i)
	pyplot.title('Original')
	pyplot.imshow(gray_im, cmap="gray")
	i += 1
	for im in im_list:
		pyplot.subplot(1, len(im_list) + 1, i)
		pyplot.title(im[1])
		pyplot.imshow(im[0], cmap='gray') 	
		i += 1
	pyplot.show()

# Upload image convert image to RGB then to gray scale
# and grab dimensions
original = cv2.imread('./James_Coleman.jpg')

rgb_pic = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
gray_im = cv2.cvtColor(rgb_pic, cv2.COLOR_RGB2GRAY)
## show([(rgb_pic, 'Color original')])

height, width = gray_im.shape	

# Filters
# Averaging 
avg1_im = numpy.zeros((height, width))
avg2_im = numpy.zeros((height, width))
avg3_im = numpy.zeros((height, width))

a_filter1 = numpy.zeros((3, 3))
a_filter1 += 1/9
a_filter2 = numpy.zeros((5, 5))
a_filter2 += 1/25
a_filter3 = numpy.zeros((11, 11))
a_filter3 += 1/121

avg1_im = cv2.filter2D(gray_im, -1, a_filter1)
avg2_im = cv2.filter2D(gray_im, -1, a_filter2)
avg3_im = cv2.filter2D(gray_im, -1, a_filter3)

show([(avg1_im, '3 x 3'),(avg2_im, '5 x 5'),(avg3_im, '11 x 11')])

# Sobel
vertical_filter = numpy.array([
	[1, 0, -1],
	[2, 0, -2],
	[1, 0, -1]
])
horizontal_filter = numpy.array([
	[1, 2, 1],
	[0, 0, 0],
	[-1, -2, -1]
])
vertical_im = cv2.filter2D(gray_im, -1, vertical_filter)
horizontal_im = cv2.filter2D(gray_im, -1, horizontal_filter)
gradient_im = numpy.maximum(vertical_im, horizontal_im)

show([(vertical_im, 'Vertical Lines'), \
	  (horizontal_im, 'Horizontal Lines'), \
	  (gradient_im, 'Gradient Lines')])

# Laplacian
four_neighbor_laplacian = numpy.array([
	[0,1,0],
	[1,-4,1],
	[0,1,0]
])
eight_neighbor_laplacian = numpy.array([
	[1,1,1],
	[1,-8,1],
	[1,1,1]
])
outline_im1 = cv2.filter2D(gray_im, -1, four_neighbor_laplacian)
outline_im2 = cv2.filter2D(gray_im, -1, eight_neighbor_laplacian)

show([(outline_im1, 'Four Neighbor Laplacian'), \
	  (outline_im2, 'Eight Neighbor Lapalcian')])

# Median
median_im = numpy.zeros((height, width))
for i in range(2, height - 2):
	for j in range(2, width - 2):
		pixel = sorted(numpy.ndarray.flatten(gray_im[i-2:i+2,j-2:j+2]))
		median_im[i][j] = pixel[12] 
show([(median_im, 'Median Filter')])
# Gaussian
small_gaussian = numpy.array(
	[[1/16,1/8,1/16],
	[1/8,1/4,1/8],
	[1/16,1/8,1/16]]
)
big_gaussian = numpy.array([
	[2,  7,  12,  7,  2],
	[7,  31, 52,  31, 7],
	[12, 52, 127, 52, 12],
	[7,  31, 52,  31, 7],
	[2,  7,  12,  7,  2]
])
biggest_gaussian = numpy.array([
	[1,1,2,2,2,1,1],
	[1,3,4,5,4,3,1],
	[2,4,7,8,7,4,2],
	[2,5,8,10,8,5,2],
	[2,4,7,8,7,4,2],
	[1,3,4,5,4,3,1],
	[1,1,2,2,2,1,1]	
])
big_gaussian = big_gaussian / numpy.sum(big_gaussian)
biggest_gaussian = biggest_gaussian / numpy.sum(biggest_gaussian)
gaussian_im1 = cv2.filter2D(gray_im, -1, small_gaussian)
gaussian_im2 = cv2.filter2D(gray_im, -1, big_gaussian)
gaussian_im3 = cv2.filter2D(gray_im, -1, biggest_gaussian)

show([(gaussian_im1, 'Small Gaussian Filter'), \
	  (gaussian_im2, 'Big Gaussian Filter'),
	  (gaussian_im3, 'Biggest Gaussian Filter')
])

# Apply two other filter
# Prewitt
vertical_prewitt = numpy.array([
	[1, 0, -1],
	[2, 0, -2],
	[1, 0, -1]
])
horizontal_prewitt = numpy.array([
	[1, 2, 1],
	[0, 0, 0],
	[-1, -2, -1]
])
vertical_prewitt_im = cv2.filter2D(gray_im, -1, vertical_prewitt)
horizontal_prewitt_im = cv2.filter2D(gray_im, -1, horizontal_prewitt)
gradient_prewitt_im = numpy.maximum(vertical_prewitt_im, horizontal_prewitt_im)

show([(vertical_im, 'Vertical Sobel Lines'), \
	  (vertical_prewitt_im, 'Vertical Prewitt Filter')]) 
show([(horizontal_im, 'Horizontal Sobel Lines'), \
 	  (horizontal_prewitt_im, 'Horizontal Prewitt Filter')])
show([(gradient_im, 'Gradient Lines'), \
	  (gradient_prewitt_im, 'Gradient Prewitt Filters')])

# Random pixel filter
random_im = numpy.zeros((height, width))
for i in range(height):
	for j in range(width):
		x = randrange(-5, 6)
		y = randrange(-5, 6)
		if (i + x >= height or i + x < 0 or j + y >= width or j + y < 0):
			random_im[i][j] = 255
		else:
			random_im[i][j] = gray_im[i + x][j + y]
show([(random_im, 'Random pixel filter')])
