from fileManagement import *
import random
import cv2

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

def steganoImage(filenameImg, msg, action, actType):
    if(action == 'hide'):
        image = readImage(filenameImg)
        pix = list(image.getdata())
        pixelFlat = [x for sets in pix for x in sets]
        message = convertMessage(msg)
        pixelList = list(range(len(pixelFlat)))
        if(actType == 'rand'):
            pixelList = randomizeList(filenameImg,pixelList)
        if(len(message) < len(pixelFlat)):
            print(pixelFlat[:5])
            pixelModified = modifyPixel(pixelFlat, message, pixelList)
        print(pixelModified[:5])
        
    elif(action == 'extractor'):
        image = readImage(filenameImg)
        message = []
    
fullDirFile = 'C:/Users/faris/OneDrive/Documents/GitHub/tugas3-kriptografi/Tugas3-Sem1-2021-2022.pdf'
fileName, byteFile = readFile(fullDirFile, isMakeMark=True)
steganoImage('blue_sky.bmp',byteFile,'hide','seq')





    





