import Tkinter as tk
import itertools as it
import random
import datetime
import time
from os import listdir

#Make list of .png files used for animation
list = listdir("romiboeyes/Romibo excited resized/")
list.sort()
list_for_romibo_excited=["romiboeyes/Romibo excited resized/"+ i for i in list]


list = listdir("romiboeyes/Romibo indifferent (short) resized/")
list.sort()
list_for_romibo_indifferentShort=["romiboeyes/Romibo indifferent (short) resized/"+ i for i in list]
#for boomerang animations
list2 = ["romiboeyes/Romibo indifferent (short) resized/"+ i for i in list]
list2.sort(reverse=True)
list_for_romibo_indifferentShort=list_for_romibo_indifferentShort+ list2

list = listdir("romiboeyes/eyelid blink/")
list.sort()
list_for_romibo_eyelidBlink=["romiboeyes/eyelid blink/"+ i for i in list]
#for boomerang animations
list2 = ["romiboeyes/eyelid blink/"+ i for i in list]
list2.sort(reverse=True)
list_for_romibo_eyelidBlink=list_for_romibo_eyelidBlink+ list2


#debug
#print(list_for_romibo_excited)

count = 0
excited_length = len(list_for_romibo_excited)
indifferentShort_length = len(list_for_romibo_indifferentShort)
blink_length = len(list_for_romibo_eyelidBlink)


#emotion letters: N = normal, E = excited, I = indifferent short
emotion = 'N'
busy = False            #Busyness of system
timestamp = time.time()
blinkInterval = 4 + random.random()*2                       #Set blink interval randomly between 4 to 6 seconds

def animate():
    """ cycle through """
    global emotion
    #If busy == False, check open emotion request file
    if busy == False:
        file = open("emotion.txt","r")
        emotion = file.read(1)
        file.close()
 
    if emotion == 'N':
        #turn on auto blink
        auto_blink()
    elif emotion == 'E':
        romibo_excited()
    elif emotion == 'I':    
        img = next(romibo_indifferentShort_pictures)            #Obtain name of next image in list
        #change image in placeholder
        label["image"] = img                                    #Change image in placeholder
        print(img)
    root.after(delay, animate)

def auto_blink():
    global label, timestamp, blinkInterval, busy, count               #To access global variables
    print (label["image"])
    if time.time()>(timestamp + blinkInterval):                     #If time is more than blink interval, trigger blink sequence
        busy = True
        if count<blink_length:
            img = next(romibo_eyelidBlink_pictures)                     #Obtain name of next image in list
            #change image in placeholder
            label["image"] = img                                    #Change image in placeholder
            count = count+1
        elif count == blink_length:
            label["image"] = romibo_normal_picture
            count = 0
            busy = False
            timestamp = time.time()
            blinkInterval = 4 + random.random()*2                       #Set blink interval randomly between 4 to 6 seconds

def romibo_excited():
    global timestamp, blinkInterval, busy, count
    if count<excited_length:
        busy = True
        img = next(romibo_excited_pictures)                     #Obtain name of next image in list
        #change image in placeholder
        label["image"] = img                                    #Change image in placeholder
        print(img)
        count = count+1
    if count == excited_length:
        count = 0
        busy = False
        label["image"] = romibo_normal_picture
        file = open("emotion.txt","w")
        file.write("N")
        file.close()
        emotion = 'N'
        timestamp = time.time()
        
            
#Essential function for tkinter
root = tk.Tk()

#Create placeholder(called a widget) to house pictures that change
label = tk.Label(root, bd = 0)

#Position widget
label.place(x=20,y=100)


# store as tk img_objects
romibo_excited_pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in list_for_romibo_excited)
romibo_indifferentShort_pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in list_for_romibo_indifferentShort)
romibo_eyelidBlink_pictures = it.cycle(tk.PhotoImage(file=img_name) for img_name in list_for_romibo_eyelidBlink)
romibo_normal_picture = tk.PhotoImage(file="romiboeyes/Romibo_normal.png")

# set initial eyes
label["image"] = romibo_normal_picture

# milliseconds
delay = 30

animate()

#Make GUI black bg and full-screen
root.configure(bg='black')
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.focus_set()  # <-- move focus to this widget

#Bind escape button
root.bind("<Escape>", lambda e: e.widget.quit())

#To prevent display lag, load images once each
for i in range(0, blink_length):
    img = next(romibo_eyelidBlink_pictures)
    print(img)
for i in range(0, excited_length):
    img = next(romibo_excited_pictures)
    print(img)
"""
for i in range(0, indifferentShort_length-1):
    img = next(romibo_indifferentShort_pictures)
    print(img)
"""
root.mainloop()