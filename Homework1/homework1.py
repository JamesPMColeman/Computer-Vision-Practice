#  
#  James Coleman
#  CS 3150
#  Homework 1
#  August 29th, 2020
#
#--------------------------------------------------
	 
	 #          >>>>>>> Goals <<<<<<<<
	 # 
	 #  1. Read in a photo
	 #  2. Remove unwanted background
	 #  3. Change the pixels in the background
	 #  4. Enhance the photo
	 #
	 #

# Imports 
import cv2
import numpy
from matplotlib import pyplot

# Helper method 
def max_of_three(i, j, k):
	""" returns the max of three """
	mot = i if (i > j) else j
	return mot if (mot > k) else k

def show(image):
	""" Helper method to display a single image 
	with pyplot """
	pyplot.imshow(image)
	pyplot.show()

# Read in the image
original = cv2.imread('./portrait2.jpg')
# show(original)

# Convert color from BGR to RGB
portrait = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
# show(portrait)

# Acquire dimensions
length, width, depth = portrait.shape
center = width  / 2

###								###
###  This section of code was added in after everything else    ###
###  was complete. It made more sense to enhance the image      ###
###  before removing background, creating a border, etc...      ###
###								###

# Enhance image
hist_eq = numpy.zeros((length, width, 3), dtype=int)
for i in range(length):
	for j in range(width):
		hist_eq[i,j,0] = portrait[i,j,0]
		hist_eq[i,j,1] = portrait[i,j,1]	
		hist_eq[i,j,2] = portrait[i,j,2]

	# Create color specific histograms
red_freq = numpy.zeros(256)
gre_freq = numpy.zeros(256)
blu_freq = numpy.zeros(256)

for i in range(length):
        for j in range(width):
                red_freq[hist_eq[i,j,0]] = red_freq[hist_eq[i,j,0]] + 1 
                gre_freq[hist_eq[i,j,1]] = gre_freq[hist_eq[i,j,1]] + 1 
                blu_freq[hist_eq[i,j,2]] = blu_freq[hist_eq[i,j,2]] + 1 

max_freq = max_of_three(red_freq.max(), gre_freq.max(), blu_freq.max())

red_sum = red_freq.cumsum()
gre_sum = gre_freq.cumsum()
blu_sum = blu_freq.cumsum()

max_sum = max_of_three(red_sum.max(), gre_sum.max(), blu_sum.max())

red_hist = red_freq * 255 / max_freq
red_cdf = red_sum * 255 / max_sum
# pyplot.plot(red_cdf, color='m')
# pyplot.plot(red_hist, color='r')

gre_hist = gre_freq * 255 / max_freq
gre_cdf = gre_sum * 255 / max_sum
# pyplot.plot(gre_cdf, color='y')
# pyplot.plot(gre_hist, color='g')

blu_hist = blu_freq * 255 / max_freq
blu_cdf = blu_sum * 222 / max_sum
# pyplot.plot(blu_cdf, color='k')
# pyplot.plot(blu_hist, color='b')
# pyplot.show()

	# Apply cdf to the all pixel intensity

for i in range(length):
	for j in range(width):
		hist_eq[i,j,0] = red_cdf[hist_eq[i,j,0]]
		hist_eq[i,j,1] = gre_cdf[hist_eq[i,j,1]]
		hist_eq[i,j,2] = blu_cdf[hist_eq[i,j,2]]

# show(hist_eq)

###					###
###          End of new code        	###
###					###

# Remove background in frame shape where the top is in the
# shape of mountains 
for i in range(length):
	for j in range(width):
		if i < abs(j - center) + 25 and \
		   i < abs(j - 222) + 45            and \
		   i < abs(j - 160) + 35            or  \
		   j < 85                           or  \
                   j > width - 70                   or  \
                   i > 370:
			# Set background as a fade from 
			# RGB(219,149,99) to saddle brown
			portrait[i,j, 0] = 219 - i / 4
			portrait[i,j, 1] = 149 - i / 4		
			portrait[i,j, 2] = 99  - i / 4

# show(portrait)

# Center image by transposing it on to new image
final = numpy.zeros((400, 300, 3), dtype=int)

for i in range(400):
	for j in range(300):
		final[i,j, 0] = portrait[i, j + 37, 0]
		final[i,j, 1] = portrait[i, j + 37, 1]
		final[i,j, 2] = portrait[i, j + 37, 2]

	# Gamma enhancement
gamma_final = final / 255
gamma_final = gamma_final ** 1.3

# show(final)
show(gamma_final)
