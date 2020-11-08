import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math
import random
 
#from skimage.measure import structural_similarity as ssim
#from sckit-image.measure import compare_ssim as ssim
#from skimage.metrics import mean_squared_error
#from skimage.metrics import peak_signal_noise_ratio
 
def add_sp_noise( src, percent):
    flat = src.ravel()
    length = len(flat)
    for ii in range(int(length * percent / 2)):
        index = int(random.random() * length)
        flat[index] = random.randint(0, 1)
    return flat.reshape(src.shape)

 
def make_g_noise( height, width , variance):
    sigmas = math.sqrt(variance)
    #noise = variance * np.random.randn(height,width)
    noise = sigmas * np.random.randn(height,width)
    return noise


def SSIM(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2

    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()

def PSNR(img1, img2):
    # img1 and img2 have range [0, 255]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))

def MSE(img1, img2):
    # img1 and img2 have range [0, 255]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
     
    return mse
##############################################################################
#                           Main Program                                     #
##############################################################################
if __name__ == "__main__":
	imA =cv.imread("./lena_g.bmp")
	imA = cv.cvtColor(imA, cv.COLOR_BGR2GRAY)
	length = imA.shape[0]
	width = imA.shape[1]

	g_noise = make_g_noise(length, width, 100)
	#u_noise = np.random.uniform(-20,20, (length, width))
	imB=imA + g_noise
	#mx=np.amax(imA)
	#mn=np.amin(imA)
	#imB=(imA-mn)/(mx-mn)*255

	mseV= MSE(imA,imB)
	psnrV = PSNR(imA, imB)
	ssimV = SSIM(imA,imB)

	plt.figure()
	plt.imshow(imB,cmap='gray')
	plt.title("MSE: %.4f, PSNR: %.4f, SSIM: %.4f" % (mseV, psnrV, ssimV))
	plt.show()
		 
