import sys
from tkinter import *
from tkinter import filedialog
import zipfile
import shutil
import os
import configparser


def setFilePath(item, item2, item3):#Sets the default folder in the ini file
    dialogFolder = filedialog.askdirectory()
    config = configparser.ConfigParser()
    config.read('organize.ini')
    config.set(item,item2, dialogFolder)
    with open('organize.ini', 'w') as configfile:
        config.write(configfile)
    print(config[item][item2])
    item3.set(getPath(item,item2)) #updates the lable so the user can se the new path


def getPath(item, item2):       #method to get a filepath from the ini file
    config = configparser.ConfigParser()
    config.read('organize.ini')
    print(config[item][item2])
    return str(config[item][item2])

def sortFolder(item,item2):
    unzip=item.get()
    sep=item2.get()
    config = configparser.ConfigParser()
    config.read('organize.ini')
    src = config['Input Folder']['defaultinputpath']

    dstZip = config['zip path']['zippath']  #Variables storing the sorting locations.
    dstExe = config['exe path']['exepath']
    dstMus = config['music path']['musicpath']
    dstImg = config['image path']['imagepath']
    dstMsc = config['misc path']['miscpath']

    dialogFolder = filedialog.askdirectory(initialdir = src, title = "Choose a Folder")
    
    print(dialogFolder)

    folder = os.listdir(dialogFolder)
    print(folder)
    for files in folder:       #sorting into a few if statements, ordered based on time to process
        print("working")
        srcFile  = str(dialogFolder)+"/"+str(files)
        print(srcFile)               

        #if statements sorting files
        if files.endswith(".zip"):
            if unzip == 1:
                zip_ref = zipfile.ZipFile(srcFile)
                zip_ref.extractall(dstZip)
                zip_ref.close()
            else:
                shutil.move(srcFile,dstZip)
        elif files.endswith(".exe"):
            shutil.move(srcFile,dstExe)
        elif files.endswith(".mp3") or files.endswith(".wav") or files.endswith(".flac") or files.endswith(".wma") or files.endswith(".m4a") or files.endswith(".m4p"):
            shutil.move(srcFile,dstMus)
        elif files.endswith(".jpg") or files.endswith(".png") or files.endswith(".gif") or files.endswith(".jpeg") or files.endswith(".bmp"):
            shutil.move(srcFile,dstImg)
        else:
            if sep == 1:
                seppath = str(dstMsc+"/Misc")
                if not os.path.exists(seppath): os.makedirs(seppath)
                shutil.move(srcFile,seppath)
            else:
                shutil.move(srcFile,dstMsc)



    
def makeWindow():
    win=Tk()
    win.title("File Sorter")

    var1=StringVar()     #All these stringvars keep the labels updated.
    var2=StringVar()
    var3=StringVar()
    var4=StringVar()
    var5=StringVar()
    var6=StringVar()
    
    cvar=IntVar()  #variables for the checkboxes
    cvar2=IntVar()

    l1 = Label(win, textvariable = var1)  #The labels that show filepaths
    l2 = Label(win,textvariable = var2)
    l3 = Label(win,textvariable = var3)
    l4 = Label(win,textvariable = var4)
    l5 = Label(win,textvariable = var5)
    l6 = Label(win,textvariable = var6)

    var1.set(getPath('Input Folder','defaultinputpath')) #initially setting the stringvars for the lables
    var2.set(getPath('exe path','exepath'))
    var3.set(getPath('music path','musicpath'))
    var4.set(getPath('image path','imagepath'))
    var5.set(getPath('misc path','miscpath'))
    var6.set(getPath('zip path','zippath'))


    #the buttons
    inputB = Button(win,text="Input Folder", command = lambda: setFilePath('Input Folder','defaultinputpath', var1)) 
    exeB = Button(win,text="Exe files", command = lambda: setFilePath('exe path','exepath', var2))
    musB = Button(win,text="Music Files", command = lambda: setFilePath('music path','musicpath', var3))
    imgB = Button(win,text="Images", command = lambda: setFilePath('image path','imagepath', var4))
    miscB = Button(win,text="Misc", command = lambda: setFilePath('misc path','miscpath', var5))
    zipB = Button(win,text="Zip Files", command = lambda: setFilePath('zip path','zippath', var6))
    orgB = Button(win,text="Organize", command = lambda: sortFolder(cvar,cvar2))

    unZip = Checkbutton(win, text ="Unzip zipped files", variable=cvar)
    sepMisc = Checkbutton(win, text ="Seperate misc files", variable=cvar2)


    #setting up the buttons and labels to look nice
    l1.grid(row=0,column=0)
    inputB.grid(row=0,column=1)
    l2.grid(row=1,column=0)
    exeB.grid(row=1,column=1)
    l3.grid(row=2,column=0)
    musB.grid(row=2,column=1)
    l4.grid(row=3,column=0)
    imgB.grid(row=3,column=1)
    l5.grid(row=4,column=0)
    miscB.grid(row=4,column=1)
    l6.grid(row=5,column=0)
    zipB.grid(row=5,column=1)
    unZip.grid(row=6)
    sepMisc.grid(row=7)
    orgB.grid(row=7, column=1)

    win.mainloop()

makeWindow()