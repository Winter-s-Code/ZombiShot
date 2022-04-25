from email.mime import image
from multiprocessing.connection import wait
from tkinter import * 
import tkinter as TK
import os



tempImg = {}
imgC = 0


#Weapon
global gWeapons
gWeapons = {}

#Using weapon
global gEquipNow
gEquipNow = {
            'Right':['SMG', 30, 4],
            'Left':['', 0, 0],
            'Helm':'',
            'UpperBody':'',
            'LowerBody':'',
            'Boots':''
            }


global allshots
allshots = []


root = Tk()
root.title('ZombiShot')
root.geometry('1200x900')
bGC = '#bfba8f'
root.configure(bg=bGC, padx=10, pady=10)
gameCanvas = Canvas(root, bg='white', height=800, width=1200)


#Get the path of the images used in the pieces
def get_path(relative_path):
    directory_path = os.path.dirname(__file__)
    file_path = os.path.join(directory_path, relative_path)
    return file_path
 

def move(event):
    global mouseX
    global mouseY
    mouseX = event.x
    mouseY = event.y
    #Create aim image for the game  
    global aimImg
    imageAim_path = get_path(r'assets\images\aim.gif')
    aimImg = PhotoImage(file=imageAim_path)
    gameCanvas.create_image(event.x, event.y, image=aimImg)   
    mpLabel.config(text='Mouse Coords: ' + 'x:' + str(event.x) + ' y:' + str(event.y))
    root.config(cursor="none")



#Create shot image for the game  
global shotImg
imageShot_path = get_path(r'assets\images\shot.gif')
shotImg = PhotoImage(file=imageShot_path)

def shot(event): 
    global shotFiredImg
    global gEquipNow
    if (gEquipNow['Right'][1] > 0):
        gameCanvas.create_image(mouseX, mouseY, image=shotImg)  
        shotFiredImg = createImg(r'assets\images\fire.gif', 730, 635)
        print('A', shotFiredImg)
        cDown()
        allshots.append(shotFiredImg)    
        gEquipNow['Right'][1] -= 1
        rightAmmoLabel.config(text='Ammo: ' + str(gEquipNow['Right'][1]))

        
    
    
def cDown(count=1):
    if count > 0 :
        gameCanvas.after(300, cDown, count-1)
    elif (count <= 0):
        gameCanvas.delete(shotFiredImg)
        print('B', shotFiredImg)
        if (shotFiredImg in allshots):
            allshots.remove(shotFiredImg)
        if (len(allshots) > 0):
            i = 0
            while i < len(allshots):
                gameCanvas.delete(allshots[i])
                i += 1 


def createImg(path, x, y):
    global tempImg
    global imgC
    imageTempPath = get_path(path)
    tempImg[imgC] = PhotoImage(file=imageTempPath)
    imgTemp = gameCanvas.create_image(x, y, image=tempImg[imgC])
    imgC += 1
    return imgTemp


global holdDown
holdDown = True


def multiShot(event):
    global holdDown
    holdDown = True
    timerDown(event)


def multiShotStop(event):
    global holdDown
    holdDown = False

    
def timerDown(event, t=0):
    global holdDown
    shot(event)
    timerLabel.config(text='Time ' + str(t))
    if (holdDown):
        gameCanvas.after(160, timerDown, event, t+1)
    else:
        pass


def autoGun(event, timer=1):
    if (timer > 0):
        gameCanvas.after(700, autoGun, event, timer-1)
    elif (timer <= 0):
        shot(event)
        return timer
    
def reloadWeap(e):
    global gEquipNow
    if (gEquipNow['Right'][2] > 0):
        gEquipNow['Right'][2] -= 1
        gEquipNow['Right'][1] = 30
        rightMagLabel.config(text='Magazines: ' + str(gEquipNow['Right'][2]))
        rightAmmoLabel.config(text='Ammo: ' + str(gEquipNow['Right'][1]))
        
mpLabel = Label(root, text='')
mpLabel.pack()


timerLabel = Label(root, text='Timer: 00')
timerLabel.pack()


rightAmmoLabel = Label(root, text='Ammo: ' + str(gEquipNow['Right'][1]))
rightAmmoLabel.pack()

rightMagLabel = Label(root, text='Magazines: ' + str(gEquipNow['Right'][2]))
rightMagLabel.pack()


createImg(r'assets\images\weapon.gif', 770, 700)



zombObj = {
            '1':{
                'typename':'easy',
                'velocity': 1,
                'dmg': 1,
                'points': 1,
                'image': r'assets\images\ezomb.gif'
                },
            '2':{
                'typename':'medium',
                'velocity': 2,
                'dmg': 2,
                'points': 3,
                'image': r'assets\images\mzomb.gif'
                },
            '3':{
                'typename':'hard',
                'velocity': 3,
                'dmg': 3,
                'points': 5,
                'image': r'assets\images\hzomb.gif'
                }
            }



#All zombies live inside this object
global zombID
zombID = {}


#Create zombies
def addZomb(x, y, type):
    if(isinstance(type, int)):
        typeC = str(type)
    else:
        typeC = type
    zo = zombObj[typeC]
    zombImgPath = get_path(zo['image'])
    global zombPI
    zombPI = PhotoImage(file=zombImgPath)
    gameCanvas.create_image(x, y, image=zombPI)
    print(zo, zombImgPath,zombPI, x, y )

addZomb(150,150,2)




gameCanvas.bind('<Motion>', move)
gameCanvas.bind('<Button-1>', shot)
gameCanvas.bind('<ButtonPress-1>', multiShot)
gameCanvas.bind('<ButtonRelease-1>', multiShotStop)
root.bind('r', reloadWeap)

gameCanvas.pack()
root.mainloop()