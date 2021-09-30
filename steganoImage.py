from fileManagement import *
import random
import cv2
from math import log10, sqrt 
import numpy as np
from PIL import Image
import tkinter.messagebox

def readImage(filename):
  img = Image.open(filename, 'r')
  return img

def convertMessage(message):
    # konversi pesan menjadi array of bit
    listByte = [val for val in message]
    bits = map(int, ''.join([bin(byte).lstrip('0b').rjust(8, '0') for byte in listByte]))
    arrayBit = list(bits)
    return arrayBit

def modifyPixel(imgList, msgList, randomList):
    # mengubah nilai pixel dengan menyisipkan bit-bit pesan pada LSB (Least Significant Byte)
    # Modify frame
    i = 0
    j = 0
    while j < len(msgList):
        if (i % 9 == 0):
            imgList[randomList[i]] = imgList[randomList[i]] & 254 | 0 # Sign if not stop msg
        else:
            imgList[randomList[i]] = imgList[randomList[i]] & 254 | msgList[j]
            j += 1
        i += 1
    imgList[randomList[i]] = imgList[randomList[i]] & 254 | 1 # Sign if stop msg
    print(i)
    print(j == len(msgList))
    return imgList

def constanta(img):
    # membuat suatu nilai konstanta
    return sum([ord(i) for i in img])

def randomizeList(filenameImg, pixel):
    # melakukan penyisipan bit pesan secara acak
    random.seed(constanta(filenameImg))
    random.shuffle(pixel)
    return pixel

def psnrImage(image,imageModified):
    # mengukur kualitas gambar setelah penyisipan pesan
    mse = np.mean((image - imageModified) ** 2)
    if mse == 0:
        return 100
    maxPixel = 255.0
    psnr = 20 * log10(maxPixel / sqrt(mse))
    return psnr

def hideSteganoImage(filenameImg, msg, actType):
    # melakukan penyisipan pesan pada gambar
        
    # membaca file gambar dan mengubah menjadi array gambar 1 dimensi
    image = readImage(filenameImg)
    arrImage = np.array(image)
    shapeImage = arrImage.shape
    pixelFlat = arrImage.ravel()
    message = convertMessage(msg)
    print(pixelFlat[:20])
    if(len(message) > len(pixelFlat)): 
        error = "Message size exceeds payload capacity!"
        tkinter.messagebox.showerror("Error", error)
        raise RuntimeError(error)
    
    # menandakan penyisipan pesan secara acak
    sign = 1 if actType == 'rand' else 0
    pixelFlat[0] = pixelFlat[0] & 254 | sign
    
    # membaca pesan dan mengubah menjadi bit-bit
    pixelList = list(range(1,len(pixelFlat)))
    if(actType == 'rand'):
        pixelList = randomizeList(filenameImg,pixelList)
    
    pixelModified = modifyPixel(pixelFlat, message, pixelList)
    print(pixelModified[:20])
    vectorImage = np.matrix(pixelModified)
    newPixel = np.asarray(vectorImage).reshape(shapeImage)
    newImage = Image.fromarray(newPixel)
    # print(newPixel)
    newImage = newImage.save('result/blue_sky.bmp')
    return newPixel

def extractSteganoImage(filenameImg):
    image = readImage(filenameImg)
    arrImage = np.array(image)
    pixelFlat = arrImage.ravel()

    randomList = list(range(1, len(pixelFlat)))
    if bin(pixelFlat[0])[-1] == '1': # isRandom
        random.seed(constanta('blue_sky.bmp'))
        random.shuffle(randomList)
    print(randomList[:5])

    # Extract to binary file
    extracted = [pixelFlat[i] & 1 for i in range(len(pixelFlat))]
    arrMsg = []
    bitMsg = ''
    i = 0
    stop = False
    while not stop:
        if i % 9 == 0 and extracted[randomList[i]] == 1:
            stop = True
        else:
            bitMsg += str(extracted[randomList[i]])
        if i % 9 == 8:
            arrMsg.append(int(bitMsg, 2))
            bitMsg = ''
        i += 1
    byteFile = bytes(arrMsg)
    print(i)
    return byteFile    
    
fullDirFile = 'C:/Users/faris/OneDrive/Documents/GitHub/tugas3-kriptografi/Tugas3-Sem1-2021-2022.pdf'
fileName, byteFile = readFile(fullDirFile, isMakeMark=True)
# pixel = hideSteganoImage('blue_sky.bmp',byteFile,'rand')
byte = extractSteganoImage('result/blue_sky.bmp')
writeFile(byte)




    





