# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:56:48 2017

@author: modellav
"""

# Image Processing

# Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from skimage import img_as_float
from skimage.restoration import nl_means_denoising
from scipy import misc
from scipy.signal import convolve2d
import math
from heapq import *




######## IMAGE DENOISING ########
######## USE SK-IMAGE ########


#function to get standard dev of noise in a B&W image
def estimate_noise(I):

  H, W = I.shape

  M = [[1, -2, 1],
       [-2, 4, -2],
       [1, -2, 1]]

  sigma = np.sum(np.sum(np.absolute(convolve2d(I, M))))
  sigma = sigma * math.sqrt(0.5 * math.pi) / (6 * (W-2) * (H-2))

  return sigma



############ DENOISE BLACK AND WHITE IMAGES ################


#read 2D image
image = misc.imread('lena_noisy.png')
shape = image.shape
image_matrix = img_as_float(image)

#estimate noise standard dev
sigma = estimate_noise(image_matrix)

#use package to denoise image
denoise_image = nl_means_denoising(image_matrix, 7, 9, sigma)

#plot noisy image and result, in black and white
fig, ax = plt.subplots(ncols=2, figsize=(8, 4), sharex=True, sharey=True,
                       subplot_kw={'adjustable': 'box-forced'})

ax[0].imshow(image_matrix, cmap = cm.Greys_r)
ax[0].axis('off')
ax[0].set_title('noisy')
ax[1].imshow(denoise_image, cmap = cm.Greys_r)
ax[1].axis('off')
ax[1].set_title('non-local means')

fig.tight_layout()

plt.show()


############ DENOISE COLOR IMAGES ################

#read 3D image
image = misc.imread('flower_0.10_noisy.jpg')
shape = image.shape
image_matrix = img_as_float(image)

#use package to denoise image
denoise_image = nl_means_denoising(image_matrix, 7, 9, 0.08)

#plot noisy image and result, in color
fig, ax = plt.subplots(ncols=2, figsize=(8, 4), sharex=True, sharey=True,
                       subplot_kw={'adjustable': 'box-forced'})

ax[0].imshow(image_matrix)
ax[0].axis('off')
ax[0].set_title('noisy')
ax[1].imshow(denoise_image)
ax[1].axis('off')
ax[1].set_title('non-local means')

fig.tight_layout()
plt.show()