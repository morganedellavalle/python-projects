# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 15:58:24 2017

@author: modellav
"""


import math
import numpy as np
from heapq import *
from scipy import misc
import matplotlib.pyplot as plt

##### IMAGE COLORING #####

colorList = []
indicesList = []

# Let's add some colored pixel to our image

# First we show our panel of colors
plot = plt.imshow(misc.imread("panel.jpg"))

# collect_points collects the color of the clicked pixel
class collect_points():
   omega = []
   def __init__(self,array):
       self.array = array
   def onclick(self,event):
       self.omega.append(plot.get_array()[int(round(event.ydata)),   int(round(event.xdata))].data)

   def indices(self):
       fig = plt.gcf()
       ax = plt.gca()
       zeta = fig.canvas.mpl_connect('button_press_event', self.onclick)
       plt.show()
       return self.omega

array = np.random.rand(10,10)*255   
colors = collect_points(array).indices()

# colorLost is the list of the clicked colors
color = (colors[0][0],colors[0][1],colors[0][2])
colorList.append(color)

# Now we wanted to indicate which pixel we want to colorize

import matplotlib.pyplot as plt

# We show our image (here a flower)
image = misc.imread("Flower.jpg")
plot = plt.imshow(image)
shape = image.shape

# We get the color chosen before
color = (colors[0][0]/255,colors[0][1]/255,colors[0][2]/255)
indices = []

# This class allows us to get the coordinates of the pixels under the mouse after a click (during motion)
class CollectCoordinates():
    
    # Initialization of the class
    def __init__(self, im):
        self.im = im

    # Connect the image to the event click motion
    def connect(self):
        'connect to all the events we need'
        self.cidmotion = fig.canvas.mpl_connect('motion_notify_event', self.on_motion)

    # Define the even motion and gather coordinates
    def on_motion(self, event):
        'on motion we will move the array if the mouse is over us'
        plt.plot(event.xdata, event.ydata, marker='o', color=color)
        
        indices.append((int(round(event.xdata)), int(round(event.ydata))))
       
        # Update the scale
        ax.set_autoscale_on = False
        ax.axis([0, shape[1]-1, shape[0]-1, 0])
        ax.set_autoscale_on = True

        # Update the plot
        fig.canvas.draw()
        
        
fig = plt.gcf()
ax = plt.gca()

# Add the coordinates to the previous one (previous color)
coord = CollectCoordinates(plt)
coord.connect()


plt.show()

indicesList.append(indices)



image = misc.imread('Flower.jpg')
shape = image.shape

# Now we compute the matrices of distances (cf report and algorithm)
dist_Matrix = []

# The pseudo-code is in the report

for c in range(0,len(colorList)):
    c_matrix = [[-1 for i in range(shape[0])] for j in range(shape[1])]

    link_list = []

    for pixel in indicesList[c]:
        c_matrix[pixel[0]][pixel[1]] = 0
        link = (0,pixel)
        heappush(link_list,link)
    
    while len(link_list) > 0:
        min_link = heappop(link_list)
        x_min = int(min_link[1][0])
        y_min = int(min_link[1][1])
        
        direction = [[1, 0], [1, 1], [1, -1], [0, 1], [0, -1], [-1, 0], [-1, 1], [-1, -1]]
        
        for i in range(0,8):
            x = x_min + direction[i][0]
            y = y_min + direction[i][1]
            
            if (x >= 0 and x < shape[1] and y >= 0 and y < shape[0]):
                
                if c_matrix[x][y] == -1:
                    c_matrix[x][y] = min_link[0] + (((direction[i][0]**2) + (direction[i][1]**2))**(1/2))*abs(image[y][x][0]-image[y_min][x_min][0])
                    heappush(link_list,(c_matrix[x][y],(x,y)))
                
    
    dist_Matrix.append(c_matrix)


# We want to change the black and white pixels into colored pixels
for x in range(0,shape[1]):
    for y in range(0,shape[0]):
        # We have to compute the denumerator of the calculation of the new color
        denum = 0
        for c in range(0, len(colorList)):
            if dist_Matrix[c][x][y] == 0:
                denum = denum + 50
            else:
                denum = denum + math.exp((-3)*math.log(dist_Matrix[c][x][y]))
        
        # We use the YCbCr colorspace instead of RGB. Y is the grayscale, Cb is Blue Difference and Cr Red Difference.
        # We compute the numerator of Cb and Cr seperatly
        PixelY = image[y][x][0]
        numCb = 0
        for c in range(0, len(colorList)):
            ColorCb = -0.1687*colorList[c][2] - 0.3313*colorList[c][1] + 0.5*colorList[c][0] + 128
            if dist_Matrix[c][x][y] == 0:
                numCb = numCb + ColorCb*50
            else:
                numCb = numCb + ColorCb*math.exp((-3)*math.log(dist_Matrix[c][x][y]))

        numCr = 0
        for c in range(0, len(colorList)):
            ColorCr = 0.5*colorList[c][2] - 0.4187*colorList[c][1] - 0.0813*colorList[c][0] + 128
            if dist_Matrix[c][x][y] == 0:
                numCr = numCr + ColorCr*50
            else:
                numCr = numCr + ColorCr*math.exp((-3)*math.log(dist_Matrix[c][x][y]))
        
        # This is the new Cb and Cr values. We already have the Y value.
        PixelCb = numCb/denum
        PixelCr = numCr/denum
        # We transform YCbCr into RGB. The transformation is linear.
        B = PixelY + 1.772*(PixelCb - 128)
        G = PixelY - 0.34414*(PixelCb - 128) - 0.71414*(PixelCr - 128)
        R = PixelY + 1.402*(PixelCr - 128)
        # We want the values to be between 0 and 255 : under 0 should be 0, over 255 should be 255.
        if B > 255:
            B = 255
        if G > 255:
            G = 255
        if R > 255:
            R = 255
        if B < 0:
            B = 0
        if G < 0:
            G = 0
        if R < 0:
            R = 0
        # We change the color of the pixel
        image[y][x] = [B,G,R]
        


# We show our new image with colors
plt.imshow(image)
plt.show()
