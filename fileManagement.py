import os.path
from os import read

def readFile(fullDirFile):
  fileName = fullDirFile[fullDirFile.rindex('/')+1:]
  markFileName = fileName + '|~FCU~|'
  f = open(fullDirFile, 'rb')
  fbyte = bytes(markFileName, 'utf-8') + f.read()
  f.close()

  return fileName, fbyte

def writeFile(fbyte):
  if (str(fbyte).find('|~FCU~|') == -1):
    fileName = 'fileText.txt'
    byteFile = fbyte
  else:
    fileName = fbyte[:str(fbyte).find('|~FCU~|')-2].decode('utf-8')
    byteFile = fbyte[str(fbyte).find('|~FCU~|')+5:]

  check = True
  tmpFilename = fileName[:fileName.rindex('.')]
  tmpExtention = fileName[fileName.rindex('.')+1:] 
  i = 0
  tmp = tmpFilename + '.' + tmpExtention
  while check:
    if (not os.path.isfile(tmp)):
      check = False
    else:
      i += 1
      tmp = tmpFilename + '(' + str(i) + ').' + tmpExtention

  fileName = tmp
  binary_file = open(fileName, "wb")
  binary_file.write(byteFile)
  binary_file.close

  return fileName