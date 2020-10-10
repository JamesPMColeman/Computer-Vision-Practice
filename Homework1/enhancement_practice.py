# Imports 
import cv2 
import numpy
from matplotlib import pyplot

# Helper method 
def show(image):
        """ Helper method to display a single image 
        with pyplot """
        pyplot.imshow(image)
        pyplot.show()

def make_histogram():
	pass

# Read in the image
original = cv2.imread('./portrait2.jpg')
# show(original)

# Convert color from BGR to RGB
portrait = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
# show(portrait)

l, w, d = portrait.shape
red_freq = numpy.zeros(256)
gre_freq = numpy.zeros(256)
blu_freq = numpy.zeros(256)

for i in range(l):
	for j in range(w):
		red_freq[portrait[i,j,0]] = red_freq[portrait[i,j,0]] + 1
		gre_freq[portrait[i,j,1]] = gre_freq[portrait[i,j,1]] + 1
		blu_freq[portrait[i,j,2]] = blu_freq[portrait[i,j,2]] + 1

red_hist = red_freq * 255 / red_freq.max()
pyplot.figure()
pyplot.plot(red_hist, color='r')
pyplot.show()
	
