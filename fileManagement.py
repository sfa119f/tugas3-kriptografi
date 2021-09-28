import os.path

def readFile(fullDirFile, isText=False, isMakeMark=False):
# Read file dengan input full directory file dan boolean apakah file adalah text (opsional)
# Output: namafile dan string pembacaan file
  fileName = fullDirFile[fullDirFile.rindex('/')+1:]
  if isText:
    f = open(fullDirFile, 'r')
    fstr = f.read()
    f.close()
    return fileName, fstr
  else:
    f = open(fullDirFile, 'rb')
    fbyte = f.read()
    f.close()
    if (isMakeMark):
      fbyte = bytes(fileName + '|~FCU~|', 'utf-8') + fbyte
    return fileName, fbyte

def writeFile(fbyte, file_name=None):
# Write file dengan input byte file dan nama file (opsional)
# Output: namafile yang disimpan
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