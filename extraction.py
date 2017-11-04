###################################
#
# (C) Aaron Renaghan
#
# Student Number: Aaron Renaghan
# Course: DT228
# Date: 13/10/2017
#
# Title: Extracting Signatures from photographs

# Introduction: This program is designed to pull signatures from photographs 
#
# Description:
# The algorithm works by going through the following steps.
# 1. Reading in the image and resizing the background to fit the signature image
# 2. Creating a mask by preforming adaptive thresholding to extract the signature
# 3. Eroding and Dilating the mask to smooth out the signature and remove noise
# 4. Creating a reverse mask and then combining masks to create our output images
# 5. Brighten up the extracted signature to try get a more true pen colour
# 6. Showing and saving the output image.
#
# My Experimentation:
# Please read here. http://228aaron.blogspot.ie/2017/10/image-processing-assignment-1.html


import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

#Reading in our images
OriginalImage = cv2.imread(easygui.fileopenbox(msg = 'Open Signature Imamge'))
background = cv2.imread(easygui.fileopenbox(msg = 'Open Background Imamge'))

#Setting the background image to be the same size as our signature.
height, width, channels = OriginalImage.shape
background = cv2.resize(background, (width,height))

#Converting OG image into greyscale for an adaptive treshold
G = cv2.cvtColor(OriginalImage, cv2.COLOR_BGR2GRAY)

#Creating a mask
B = cv2.adaptiveThreshold(G, maxValue = 255, adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType = cv2.THRESH_BINARY, blockSize = 31,C = 11)

#Eroding a dilating the image to remove imperfections
shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
B = cv2.erode(B,shape) 
B = cv2.dilate(B,shape)

#Creating a reverse mask
BN = cv2.bitwise_not(B)

#Extracting the Signature
signature = cv2.bitwise_and(OriginalImage, OriginalImage, mask=BN)
background = cv2.bitwise_and(background, background, mask=B)

#Color Enchancement kinda :/
yuv = cv2.cvtColor(signature, cv2.COLOR_BGR2YUV)
yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
signature = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

#Combining our signatures into a image which can be dropped into documents
finalImage = cv2.bitwise_or(signature, background)


# Showing the final extracted signature and saving to a file for future mischievous use
cv2.imshow("Extracted Signature", finalImage)
cv2.imwrite('extractedSignature.png', finalImage)

cv2.waitKey(0)
