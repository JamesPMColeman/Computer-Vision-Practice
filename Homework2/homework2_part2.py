#=============================================================================#
#                                                                             #
#   James Coleman                                                             #
#   CS 3150                                                                   #
#   Homework 2 part one                                                       #
#   September 26th                                                            #
#                                                                             #
#=============================================================================#

        #              >>>>>>>>>> Goals <<<<<<<<<<
        #   
        #   1.  Smooth out the iris image to suppress small 
        #       edges.
        #   2.  Produce edges of the image using Sobal filters
        #       and gradient
        #   3.  Detect the center of the of the eye
        #   4.  Detect the boundary of the eye (radius is 
        #       roughly 35 to 45 pixels)
        #   
        #

# Imports
import cv2
import math
import numpy
from scipy.signal import convolve2d
from matplotlib import pyplot
# Helper methods
def show(image, name):
    pyplot.figure()
    pyplot.title(name)
    pyplot.imshow(image, cmap="gray", vmin=0, vmax=255)
    pyplot.show()
# Acquire the image and display
original = cv2.imread('./iris.bmp')
eye = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
h, w = eye.shape
show(eye, "Original") 

# Blur the image
avg_filter = numpy.zeros((7, 7))                    ## Create a 15 by 15
avg_filter += 1/(7 * 7)                             ## average filter.
avg_eye = cv2.filter2D(eye, -1, avg_filter)         ## Apply filter. 

show(avg_eye, "Smoothed Eye")	                    ## Displayed averaged image

# Detect edges
vt_filter = numpy.array([                           ## create vertical and 
    [1, 0, -1],                                     ## horizontal sobal filters
    [2, 0, -2],
    [1, 0, -1]  
])
ht_filter = numpy.array([
    [1, 2, 1],
    [0, 0, 0],
    [-1, -2, -1]
])
vt_eye = convolve2d(avg_eye, vt_filter)             ## apply filters
ht_eye = convolve2d(avg_eye, ht_filter)

show(vt_eye, "Vertical Sobal")
show(ht_eye, "Horizontal Sobal")

gradient = numpy.sqrt(                              ## Create new image to be 
    numpy.square(vt_eye) +                          ## the square root of the 
    numpy.square(ht_eye)                            ## vertical and horizontal 
)                                                   ## image squared and summed

show(gradient, "Sobal Gradient")                    ## Display gradient image

# Detect the focus of the eye
r1 = 45                                             ## Create a ring filter 
r2 = 35                                             ## with outer radius 45 and
ring = numpy.zeros((120, 120))                      ## inner radius 35

for i in range(120):
    for j in range(120):
        if math.sqrt((i - 60)**2 + (j - 60)**2) < r1 and \
           math.sqrt((i - 60)**2 + (j - 60)**2) > r2:
            ring[i][j] = 1
### show(ring) ###                                  ## apply filter

pupil_focus = convolve2d(gradient, ring, mode="same", boundary="symm") 
pupil_focus = numpy.absolute(pupil_focus)
pupil_focus *= 255 / numpy.max(pupil_focus)

show(pupil_focus, "Ring Filtered")

a_focus = 0
b_focus = 0
intense = 0

for i in range(45, h-45):                           ## acquire the coordinates 
    for j in range(45, w-45):                       ## of the maximum
        if pupil_focus[i][j] > intense: 
            a_focus = i
            b_focus = j
            intense = pupil_focus[i][j]

### show(focus) ### 

for i in range(h):                                  ## super impose the focus 
    for j in range(w):                              ## image (just the center
        if math.sqrt((i - a_focus)**2 +             ## dot) on to the gradient
                     (j - b_focus)**2) < 3:         ## image
            gradient[i][j] = 255             

show(gradient, "Focus")

# Detect the boundary of the circle.
for i in range(h):
    for j in range(w): 
        if math.sqrt((i - a_focus + 2)**2 +             
                     (j - b_focus + 2)**2) < 38 and \
           math.sqrt((i - a_focus + 2)**2 +             
                     (j - b_focus + 2)**2) > 37:         
            eye[i][j] = 255             
            
# Display results
show(eye, "Pupil boundary")             
