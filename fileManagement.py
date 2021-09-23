import os.path
from os import read

def readFile(fullDirFile, isText=False):
  fileName = fullDirFile[fullDirFile.rindex('/')+1:]
  f = open(fullDirFile, 'rb')
  fbyte = f.read()
  f.close()
  if not isText:
    fbyte = bytes(fileName + '|~FCU~|', 'utf-8') + fbyte
  fstr = str(fbyte)
  fstr = fstr[2:len(fstr)-1]

  return fileName, fstr

def writeFile(fbyte, file_name=None):
  if (str(fbyte).find('|~FCU~|') == -1):
    fileName = file_name if file_name is not None else 'fileResultText.txt'
    byteFile = fbyte
  else:
    fileName = fbyte[:str(fbyte).find('|~FCU~|')-2].decode()
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