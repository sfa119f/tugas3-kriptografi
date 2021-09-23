from os import read
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from fileManagement import *

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
rc4 = Toplevel(home)
rc4.title('Modified RC4')
rc4.geometry('200x150')
rc4.geometry("+{}+{}".format(
  int((rc4.winfo_screenwidth()-200) / 2), int((rc4.winfo_screenheight()-150) / 2)
))
rc4.protocol("WM_DELETE_WINDOW", disable_event)
rc4.resizable(0,0)

Button(rc4, text='Home', font=('Calibri', 12, 'bold'), width=7, command=home_win, bg='RoyalBlue1').place(x=10, y=10)
Button(rc4, text='Close', font=('Calibri', 12, 'bold'), width=7, command=close_win, bg='red2').place(x=90, y=10)

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
  if (stegAction.get() == 'hide'):
    stegSeqRad.config(state=NORMAL)
    stegRandRad.config(state=NORMAL)
    stegActType.set('seq')
    stegProcessBtn.config(text='Hide Message Now!')
  else:
    stegActType.set('X')
    stegSeqRad.config(state=DISABLED)
    stegRandRad.config(state=DISABLED)
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
  elif stegMsg.get() == '':
    tkinter.messagebox.showinfo('Error', 'Message file is not available')
  else:
    try:
      if stegEncryptMode.get() and stegAction.get() == 'hide':
        # encrypt message
        print('encrypt message')
      if stegMediaType.get() == 'image':
        # result = methodStegImage(stegAction.get(), stegMedia.get(), stegMsg.get())
        tkinter.messagebox.showinfo('Success', 'Success Pocess Steganografi in Image')
      else:
        # result = methodStegAudio(stegAction.get(), stegMedia.get(), stegMsg.get())
        tkinter.messagebox.showinfo('Success', 'Success Pocess Steganografi in Audio')
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
Button(steg, text='Import File', command=importStegMsg, bg='grey85', width=8).place(x=10, y=300)

stegProcessBtn = Button(steg, text='Hide Message Now!', font=('Calibri', 12, 'bold'), command=processSteg, bg='RoyalBlue1', width=20)
stegProcessBtn.place(x=80, y=350)

Button(steg, text='Reset', font=('Calibri', 12, 'bold'), command=stegReset, bg='red2', width=7).place(x=130, y=395)

steg.withdraw()

# ------------------------- Looping Program ------------------------- #
mainloop()