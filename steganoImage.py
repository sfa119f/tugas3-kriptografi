from fileManagement import *
import random
import cv2
from math import log10, sqrt 
import numpy as np

def convertMessage(message):
    listByte = [val for val in message]
    bits = map(int, ''.join([bin(byte).lstrip('0b').rjust(8, '0') for byte in listByte]))
    arrayBit = list(bits)
    return arrayBit

def modifyPixel(pixelList, msgList, randomList):
    for i in range (len(msgList)):
        if(msgList[i] == 0 and pixelList[randomList[i]] % 2 != 0):
            pixelList[randomList[i]] -= 1
        elif(msgList[i] == 1 and pixelList[randomList[i]] % 2 == 0):
            if(pixelList[randomList[i]] != 0):
                pixelList[randomList[i]] -= 1
            else:
                pixelList[randomList[i]] += 1
    return pixelList

def constanta(img):
    return sum([ord(i) for i in img])

def randomizeList(filenameImg, pixel):
    random.seed(constanta(filenameImg))
    random.shuffle(pixel)
    return pixel

def psnrImage(image,imageModified):
    mse = np.mean((image - imageModified) ** 2)
    if mse == 0:
        return 100
    maxPixel = 255.0
    psnr = 20 * log10(maxPixel / sqrt(mse))
    return psnr

def hideSteganoImage(filenameImg, msg, actType):
    image = readImage(filenameImg)
    arrImage = np.array(image)
    shapeImage = arrImage.shape
    pixelFlat = arrImage.ravel()
    message = convertMessage(msg)
    print(message[:20])
    pixelList = list(range(len(pixelFlat)))
    if(actType == 'rand'):
        pixelList = randomizeList(filenameImg,pixelList)
    if(len(message) < len(pixelFlat)):
        pixelModified = modifyPixel(pixelFlat, message, pixelList)
    vectorImage = np.matrix(pixelModified)
    newPixel = np.asarray(vectorImage).reshape(shapeImage)
    # newImage = Image.fromarray(newPixel)
    # print(newImage)
    # newImage = newImage.save('blue_sky1.bmp')
    return newPixel

def extractSteganoImage(filenameImg, actType):    
    image = readImage(filenameImg)
    arrImage = np.array(image)
    pixelFlat = arrImage.ravel()
    message = []
    msgBinary = []
    for i in range (len(pixelFlat)):
        if(i % 2 == 0):
            msgBinary.append(0)
        else:
            msgBinary.append(1)
    print(msgBinary[:20])
    return message
    
fullDirFile = 'C:/Users/faris/OneDrive/Documents/GitHub/tugas3-kriptografi/Tugas3-Sem1-2021-2022.pdf'
fileName, byteFile = readFile(fullDirFile, isMakeMark=True)
pixel = hideSteganoImage('blue_sky.bmp',byteFile,'seq')
message = extractSteganoImage('blue_sky1.bmp','seq')




    





