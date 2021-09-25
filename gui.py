from os import read
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from fileManagement import *
from rc4Cipher import methodRc4

def home_win():
  home.deiconify()
  rc4.withdraw()
  steg.withdraw()

def rc4_win():
  home.withdraw()
  rc4.deiconify()
  steg.withdraw()

def steg_win():
  home.withdraw()
  rc4.withdraw()
  steg.deiconify()

def close_win():
  steg.destroy()
  rc4.destroy()
  home.destroy()

def disable_event():
  pass

# ------------------------- Windows Home ------------------------- #
home = Tk()
home.title('Home')
home.geometry('220x150')
home.geometry("+{}+{}".format(
  int((home.winfo_screenwidth()-220) / 2), int((home.winfo_screenheight()-150) / 2)
))
home.resizable(0,0)

Label(home, text='Choose Task:', font=('Calibri', 14, 'bold')).place(x=5, y=5)
Button(home, text='Modified RC4', font=('Calibri', 12, 'bold'), width=14, command=rc4_win, bg='RoyalBlue1').place(x=50, y=45)
Button(home, text='Steganografi', font=('Calibri', 12, 'bold'), width=14, command=steg_win, bg='RoyalBlue1').place(x=50, y=95)

# ------------------------- Windows RC4 ------------------------- #
# Method
def setRc4FileBtn():
  if (rc4ImportType.get()):
    rc4FileBtn.config(state=NORMAL)
    inputRc4.delete('1.0', END)
    inputRc4.config(state=DISABLED)
    outputRc4.config(state=NORMAL)
    outputRc4.delete('1.0', END)
    outputRc4.config(state=DISABLED)
    saveBtnRc4.config(state=DISABLED)
  else:
    labelRc4File.config(text='')
    rc4FileBtn.config(state=DISABLED)
    inputRc4.config(state=NORMAL)
    saveBtnRc4.config(state=NORMAL)

def importRc4File():
  try:
    fullDirFile = filedialog.askopenfile().name
    if fullDirFile[fullDirFile.rindex('.')+1:] == 'txt':
      isInputFileRc4Text.set(True)
      fileName, fstr = readFile(fullDirFile, True)
      inputRc4.config(state=NORMAL)
      inputRc4.insert(tkinter.END, fstr)
      inputRc4.config(state=DISABLED)
    else:
      fileName, fbyte = readFile(fullDirFile)
      rc4FileByte.set(fbyte)
    labelRc4File.config(text=fileName)
    tkinter.messagebox.showinfo('Success', 'Success import: ' + fileName)
    if keyRc4.get('1.0', 'end-1c') != '':
      processRc4()
  except:
    tkinter.messagebox.showinfo('Error', 'Something went wrong when import file')

def copyOutputRc4():
  try:
    if outputRc4.get('1.0', 'end-1c') == '':
      raise Exception()
    rc4.clipboard_clear()
    rc4.clipboard_append(outputRc4.get('1.0', 'end-1c'))
    rc4.update()
    tkinter.messagebox.showinfo('Success', 'Copied to clipboard')
  except:
    tkinter.messagebox.showinfo('Error', 'No value is copied')

def saveOutputRc4():
  try:
    res = "Input:\n" + inputRc4.get('1.0', 'end-1c') + '\nOutput:\n' + outputRc4.get('1.0', 'end-1c')
    fbyte = bytes(res, 'utf-8')
    fileName = writeFile(fbyte)
    tkinter.messagebox.showinfo('Success', 'Success export result to: '+ fileName)
  except:
    tkinter.messagebox.showinfo('Error', 'Error when export result to file')

def rc4Reset():
  rc4ImportType.set(False)
  setRc4FileBtn()
  rc4FileByte.set('')
  keyRc4.delete('1.0', END)
  inputRc4.delete('1.0', END)
  outputRc4.config(state=NORMAL)
  outputRc4.delete('1.0', END)
  outputRc4.config(state=DISABLED)
  isInputFileRc4Text.set(False)

def processRc4():
  outputRc4.config(state=NORMAL)
  outputRc4.delete('1.0', END)
  outputRc4.config(state=DISABLED)
  if keyRc4.get('1.0', 'end-1c') == '':
    tkinter.messagebox.showinfo('Error', 'Key not available')
  elif rc4FileByte.get() == '' and rc4ImportType.get() and not isInputFileRc4Text.get():
    tkinter.messagebox.showinfo('Error', 'Input file not available')
  elif inputRc4.get('1.0', 'end-1c') == '' and (not rc4ImportType.get() or isInputFileRc4Text.get()):
    tkinter.messagebox.showinfo('Error', 'Input not available')
  else:
    try:
      if rc4ImportType.get() and not isInputFileRc4Text.get():
        # result = methodRc4(rc4Mode.get(), keyRc4.get('1.0', 'end-1c'), rc4FileByte.get())
        # fileName = writeFile(bytes(rc4FileByte.get(), 'utf-8'), 'test.bin')
        # tkinter.messagebox.showinfo('Success', 'Success export result to: '+ fileName)
        tkinter.messagebox.showinfo('Error', 'Encrypt/decrypt using binary files has not been implemented')
        saveBtnRc4.config(state=DISABLED)
      else:
        result = methodRc4(keyRc4.get('1.0', 'end-1c'), inputRc4.get('1.0', 'end-1c'))
        outputRc4.config(state=NORMAL)
        outputRc4.insert(tkinter.END, result)
        outputRc4.config(state=DISABLED)
        tkinter.messagebox.showinfo('Success', 'Success Process RC4 Algorithm')
        saveBtnRc4.config(state=NORMAL)
      isInputFileRc4Text.set(False)
    except:
      tkinter.messagebox.showinfo('Error', 'Something went wrong when processing RC4 Algorithm')

#GUI
rc4 = Toplevel(home)
rc4.title('Modified RC4')
rc4.geometry('360x580')
rc4.geometry("+{}+{}".format(
  int((rc4.winfo_screenwidth()-360) / 2), int((rc4.winfo_screenheight()-580) / 2) - 20
))
rc4.protocol("WM_DELETE_WINDOW", disable_event)
rc4.resizable(0,0)

rc4FileByte = StringVar(rc4)
isInputFileRc4Text = BooleanVar(rc4, False)

Button(rc4, text='Home', font=('Calibri', 12, 'bold'), width=7, command=home_win, bg='RoyalBlue1').place(x=10, y=10)
Button(rc4, text='Close', font=('Calibri', 12, 'bold'), width=7, command=close_win, bg='red2').place(x=280, y=10)

Label(rc4, text='RC4 Mode:').place(x=10, y=60)
rc4Mode = BooleanVar(rc4, True)
Radiobutton(rc4, text='Encrypt', variable=rc4Mode, value=True, state=DISABLED).place(x=75, y=60)
Radiobutton(rc4, text='Decrypt', variable=rc4Mode, value=True, state=DISABLED).place(x=170, y=60)

Label(rc4, text='Import File:').place(x=10, y=90)
rc4ImportType = BooleanVar(rc4, False)
Radiobutton(rc4, text='Without File', variable=rc4ImportType, value=False, command=setRc4FileBtn).place(x=75, y=90)
Radiobutton(rc4, text='Using File', variable=rc4ImportType, value=True, command=setRc4FileBtn).place(x=170, y=90)

rc4FileBtn = Button(rc4, text='Import', command=importRc4File, bg='grey85', width=8, state=DISABLED)
rc4FileBtn.place(x=10, y=110)
labelRc4File = Label(rc4, font=('Calibri', 10, 'underline'), fg='blue')
labelRc4File.place(x=80, y=110)

Label(rc4, text='Key:').place(x=10, y=140)
keyRc4 = ScrolledText(rc4, height=1, width=40)
keyRc4.place(x=10, y=160)

Label(rc4, text='Input:').place(x=10, y=220)
inputRc4 = ScrolledText(rc4, height=5, width=40)
inputRc4.place(x=10, y=240)

Label(rc4, text='Output:').place(x=10, y=335)
outputRc4 = ScrolledText(rc4, height=5, width=40, state=DISABLED)
outputRc4.place(x=10, y=355)

Button(rc4, text='Copy', command=copyOutputRc4, bg='grey85', width=7).place(x=10, y=440)
saveBtnRc4 = Button(rc4, text='Save', command=saveOutputRc4, bg='grey85', width=7, state=DISABLED)
saveBtnRc4.place(x=290, y=440)

Button(rc4, text='Encrypt/Decrypt Now!', font=('Calibri', 12, 'bold'), command=processRc4, bg='RoyalBlue1', width=20).place(x=95, y=480)

Button(rc4, text='Reset', font=('Calibri', 12, 'bold'), command=rc4Reset, bg='red2', width=7).place(x=155, y=525)

rc4.withdraw()

# ------------------------- Windows Steganografi ------------------------- #
# Method
def showStegKey():
  if (stegEncryptMode.get()):
    keySteg.config(state=NORMAL)
  else:
    keySteg.delete('1.0', END)
    keySteg.config(state=DISABLED)

def importMediaSteg():
  try:
    fullFileName = filedialog.askopenfile().name
    fileName = fullFileName[fullFileName.rindex('/')+1:]
    f = open(fullFileName, 'rb')
    stegMedia.set(f.read())
    f.close()
    labelStegMedia.config(text=fileName)
    tkinter.messagebox.showinfo('Success', 'Success import: ' + fileName)
  except:
    tkinter.messagebox.showinfo('Error', 'Something went wrong when import file')

def showStegActType():
  if stegAction.get() == 'hide':
    stegSeqRad.config(state=NORMAL)
    stegRandRad.config(state=NORMAL)
    importStegMsgBtn.config(state=NORMAL)
    stegActType.set('seq')
    stegProcessBtn.config(text='Hide Message Now!')
  else:
    stegActType.set('X')
    stegSeqRad.config(state=DISABLED)
    stegRandRad.config(state=DISABLED)
    importStegMsgBtn.config(state=DISABLED)
    labelStegMsg.config(text='')
    stegProcessBtn.config(text='Extract Message Now!')

def importStegMsg():
  try:
    fullDirFile = filedialog.askopenfile().name
    fileName, fbyte = readFile(fullDirFile)
    stegMsg.set(fbyte)
    labelStegMsg.config(text=fileName)
    tkinter.messagebox.showinfo('Success', 'Success import: ' + fileName)
  except:
    tkinter.messagebox.showinfo('Error', 'Something went wrong when import file')

def stegReset():
  stegEncryptMode.set(False)
  showStegKey()
  stegAction.set('hide')
  showStegActType()
  stegMediaType.set('image')
  stegMedia.set('')
  stegMsg.set('')

def processSteg():
  if stegEncryptMode.get() and keySteg.get('1.0', 'end-1c') == '':
    tkinter.messagebox.showinfo('Error', 'Key is empty')
  elif stegMedia.get() == '':
    tkinter.messagebox.showinfo('Error', 'Multimedia file is not available')
  elif stegAction.get() == 'hide' and stegMsg.get() == '':
    tkinter.messagebox.showinfo('Error', 'Message file is not available')
  else:
    try:
      if stegEncryptMode.get() and stegAction.get() == 'hide':
        # encrypt message
        print('encrypt message')
      if stegMediaType.get() == 'image':
        # result = methodStegImage(stegAction.get(), stegMedia.get(), stegMsg.get())
        tkinter.messagebox.showinfo('Success', 'Success Process Steganografi in Image')
      else:
        # result = methodStegAudio(stegAction.get(), stegMedia.get(), stegMsg.get())
        tkinter.messagebox.showinfo('Success', 'Success Process Steganografi in Audio')
      if stegEncryptMode.get() and stegAction.get() == 'extract':
        # decrypt result
        print('decrypt result')
      # if stegAction.get() == 'hide': # Export File
      #   result = bytes('aku anak Indonesia', 'utf-8')
      #   fileName = writeFile(result)
      #   tkinter.messagebox.showinfo('Success', 'Success export result to: '+ fileName)
    except:
      tkinter.messagebox.showinfo('Error', 'Something went wrong when processing steganografi')

# GUI
steg = Toplevel(home)
steg.title('Steganografi')
steg.geometry('330x450')
steg.geometry("+{}+{}".format(
  int((steg.winfo_screenwidth()-330) / 2), int((steg.winfo_screenheight()-450) / 2)
))
steg.protocol("WM_DELETE_WINDOW", disable_event)
steg.resizable(0,0)

stegMedia = StringVar(steg)
stegMsg = StringVar(steg)

Button(steg, text='Home', font=('Calibri', 12, 'bold'), width=7, command=home_win, bg='RoyalBlue1').place(x=10, y=10)
Button(steg, text='Close', font=('Calibri', 12, 'bold'), width=7, command=close_win, bg='red2').place(x=250, y=10)

Label(steg, text='Encryption Mode:').place(x=10, y=60)
stegEncryptMode = BooleanVar(steg, False)
Radiobutton(steg, text='Without Encryption', variable=stegEncryptMode, value=False, command=showStegKey).place(x=10, y=80)
Radiobutton(steg, text='Using Encryption', variable=stegEncryptMode, value=True, command=showStegKey).place(x=10, y=100)

Label(steg, text='Key:').place(x=180, y=60)
keySteg = ScrolledText(steg, height=3, width=15, state=DISABLED)
keySteg.place(x=180, y=80)

Label(steg, text='Multimedia File:').place(x=10, y=140)
labelStegMedia = Label(steg, font=('Calibri', 10, 'underline'), fg='blue')
labelStegMedia.place(x=100, y=140)
stegMediaType = StringVar(steg, 'image')
Radiobutton(steg, text='Image', variable=stegMediaType, value='image').place(x=10, y=160)
Radiobutton(steg, text='Audio', variable=stegMediaType, value='audio').place(x=90, y=160)

mediaSteg = Button(steg, text='Import File', command=importMediaSteg, bg='grey85', width=8)
mediaSteg.place(x=180, y=160)

Label(steg, text='Action:').place(x=10, y=200)
stegAction = StringVar(steg, 'hide')
Radiobutton(steg, text='Hide Message', variable=stegAction, value='hide', command=showStegActType).place(x=10, y=220)
Radiobutton(steg, text='Extract Message', variable=stegAction, value='extract', command=showStegActType).place(x=10, y=240)

Label(steg, text='Action Type:').place(x=180, y=200)
stegActType = StringVar(steg, 'seq')
stegSeqRad = Radiobutton(steg, text='Sequential', variable=stegActType, value='seq')
stegSeqRad.place(x=180, y=220)
stegRandRad = Radiobutton(steg, text='Random', variable=stegActType, value='rand')
stegRandRad.place(x=180, y=240)

Label(steg, text='Message File:').place(x=10, y=280)
labelStegMsg = Label(steg, font=('Calibri', 10, 'underline'), fg='blue')
labelStegMsg.place(x=85, y=280)
importStegMsgBtn = Button(steg, text='Import File', command=importStegMsg, bg='grey85', width=8)
importStegMsgBtn.place(x=10, y=300)

stegProcessBtn = Button(steg, text='Hide Message Now!', font=('Calibri', 12, 'bold'), command=processSteg, bg='RoyalBlue1', width=20)
stegProcessBtn.place(x=80, y=350)

Button(steg, text='Reset', font=('Calibri', 12, 'bold'), command=stegReset, bg='red2', width=7).place(x=130, y=395)

steg.withdraw()

# ------------------------- Looping Program ------------------------- #
mainloop()