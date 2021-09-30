from fileManagement import *
import random
from math import log10, sqrt 
import numpy as np
import tkinter.messagebox

def convertMessage(message):
    # Konversi pesan menjadi array of bit
    listByte = [val for val in message]
    bits = map(int, ''.join([bin(byte).lstrip('0b').rjust(8, '0') for byte in listByte]))
    arrayBit = list(bits)
    return arrayBit

def modifyPixel(imgList, msgList, randomList):
    # Mengubah nilai pixel dengan menyisipkan bit-bit pesan pada LSB (Least Significant Byte)
    # Modify pixel
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
    return imgList

def constanta(img):
    # Membuat suatu nilai konstanta untuk penyisipan pesan secara acak
    return sum([ord(i) for i in img])

def randomizeList(filenameImg, pixel):
    # Melakukan penyisipan bit pesan secara acak
    random.seed(constanta(filenameImg))
    random.shuffle(pixel)
    return pixel

def psnrImage(image,imageModified):
    # Mengukur kualitas gambar setelah penyisipan pesan
    mse = np.mean((image - imageModified) ** 2)
    if mse == 0:
        return 100
    maxPixel = 255.0
    psnr = 20 * log10(maxPixel / sqrt(mse))
    return psnr

def hideSteganoImage(filenameImg, msg, image, actType):
    # Melakukan penyisipan pesan pada gambar
        
    # Membaca file gambar dan mengubah menjadi array gambar 1 dimensi
    arrImage = np.array(image)
    shapeImage = arrImage.shape
    pixelFlat = arrImage.ravel()
    message = convertMessage(msg)
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
    vectorImage = np.matrix(pixelModified)
    newPixel = np.asarray(vectorImage).reshape(shapeImage)
    return newPixel

def extractSteganoImage(filenameImg, image):
    # Melakukan ekstraksi pesan dari stego image
    arrImage = np.array(image)
    pixelFlat = arrImage.ravel()
    randomList = list(range(1, len(pixelFlat)))
    if bin(pixelFlat[0])[-1] == '1': # isRandom
        random.seed(constanta('blue_sky.bmp'))
        random.shuffle(randomList)

    # Ekstraksi binary file
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
    return byteFile    

def methodStegImage(action, actType, filenameImg, image, file):
    # Fungsi utama steganografi
    # Output: pixel image dan byte file
    if action == 'hide':
        resPixel = hideSteganoImage(filenameImg, file, image, actType)
        return resPixel, None
    else:
        byteFile = extractSteganoImage(filenameImg, image)
        return [], byteFile 