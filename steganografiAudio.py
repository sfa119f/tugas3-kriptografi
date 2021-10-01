import numpy as np
import random
import tkinter.messagebox

def countSeed(text):
# Menghitung seed untuk dari text untuk keperluan random
  return sum([ord(i) for i in text])

def hideAudio(actType, audioname, frame, file):
# Menyembunyikan file ke audio
# Output: frame audio
  if len(frame) // 9 < len(file): # check frame >= file, 9 byte frame for 1 byte file
    error = "Message size exceeds payload capacity!"
    tkinter.messagebox.showerror("Error", error)
    raise RuntimeError(error)
  
  # List byte file to list bit file
  listByte = [val for val in file]
  bits = map(int, ''.join([bin(byte).lstrip('0b').rjust(8, '0') for byte in listByte]))
  bitMsg = list(bits)

  frameList = list(range(1, len(frame)))

  # Random frame
  sign = 1 if actType == 'rand' else 0
  frame[0] = frame[0] & 254 | sign
  if actType == 'rand':
    random.seed(countSeed(audioname))
    random.shuffle(frameList)

  # Modify frame
  i = 0
  j = 0
  while j < len(bitMsg):
    if (i % 9 == 0):
      frame[frameList[i]] = frame[frameList[i]] & 254 | 0 # Sign if not stop msg
    else:
      frame[frameList[i]] = frame[frameList[i]] & 254 | bitMsg[j]
      j += 1
    i += 1
  frame[frameList[i]] = frame[frameList[i]] & 254 | 1 # Sign if stop msg

  return frame

def extractAudio(audioname, frame):
# Mengekstrak file dari audio
# Output: byte file
  frameList = list(range(1, len(frame)))
  if bin(frame[0])[-1] == '1': # isRandom
    random.seed(countSeed(audioname))
    random.shuffle(frameList)

  # Extract to binary file
  extracted = [frame[i] & 1 for i in range(len(frame))]
  arrMsg = []
  bitMsg = ''
  i = 0
  stop = False
  while not stop:
    if i % 9 == 0 and extracted[frameList[i]] == 1:
      stop = True
    else:
      bitMsg += str(extracted[frameList[i]])
      if i % 9 == 8:
        arrMsg.append(int(bitMsg, 2))
        bitMsg = ''
    i += 1
  byteFile = bytes(arrMsg)

  return byteFile

def methodStegAudio(action, actType, audioname, frame, file):
# Fungsi utama steganografi
# Output: frame audio dan byte file
  if action == 'hide':
    resFrame = hideAudio(actType, audioname, frame, file)
    return resFrame, None
  else:
    byteFile = extractAudio(audioname, frame)
    return None, byteFile

def fidelityAudio(audio, audioModified):
# Mengukur kualitas audio setelah penyisipan pesan
  audioSize = len(audio)
  mse = np.sum(pow(audio[i] - audioModified[i], 2) for i in range(audioSize)) / audioSize
  maxAudio = np.sum(pow(audioModified[i], 2) for i in range(audioSize)) / audioSize
  fidelity = 10 * np.log10(maxAudio / mse)
  
  return fidelity