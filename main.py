# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#    Platform        : main.py
#    Project Name    : Automatic Parking + Detection Of Empty Places
#    Author          : Anouar Asmai - Mohamed Elhamra - Abdennacer Elmaalem - Manal El-rhezzali - Yassine Zougagh - Sohaib Sghir
#------------------------------------------------------------------------------

#-----------------------------import lib---------------------------------------
import telepot
import time
import cv2
import numpy as np

#------------------------------------------------------------------------------

#---------------------------Camera Image Take---------------------------------
def capture_img():
    camera_port = 1
    ramp_frames = 30
    camera = cv2.VideoCapture(0)

    def get_image():
        retval, im = camera.read()
        return im

    print("Taking image...")
    camera_capture = get_image()
#saving current image in process_img.png
    file = "process_img.png"
    cv2.imwrite(file, camera_capture)
#------------------------------------------------------------------------------

#--------------------------Canny Edge Algorithm--------------------------------
# Algorithme de Canny : 1-Réduction de bruit avec un filtre gaussien
#---------------------- 2-Recherche du gradient d'intensité de l'image (sobel)
#---------------------- 3-Suppression non maximale pour supprimer tous les pixels indésirables qui pourraient ne pas constituer le bord
#---------------------- 4-Seuil d'hystérésis : Cette étape décide quels sont tous les bords qui sont vraiment des bords et lesquels ne le sont pas

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged
#------------------------------------------------------------------------------


#-------------------------Count fuction for white pixels (1) calculation------------------
def cal_count(edges,x1,y1,x2,y2):
    #global edges
    count=0

    for y in range(y1,y2):
        for x in range(x1,x2):
            if edges[y][x] != 0:
                #print "[",x,"]","[",y,"] =",edges[x][y]
                count+=1
    return count
#------------------------------------------------------------------------------

def solt_info():
    img = cv2.imread('process_img.png',0)     #import img
  
    # Find Canny edges 
    edged = auto_canny(img) 
  
    #cv2.imshow(edges)             #send for canny edges calculation
    #height = np.size(img, 0)
    #width = np.size(img, 1)
    
    
    #specifie the edges of every place in the Parking (our example : 6 places)
    #print every value to compare it with the sure-edge "seuil"

    #cv2.rectangle(edges, (20, 35), (230, 210), (255,0,0), 2) 
    slot_1=cal_count(edged, 7, 0, 228, 113)
    print(slot_1)
    #cv2.rectangle(edges, (8, 240), (230, 430), (255,0,0), 2)
    slot_2=cal_count(edged, 1, 174, 234, 288)
    print(slot_2)
    #cv2.rectangle(edges, (410, 195), (605, 20), (255,0,0), 2)
    slot_3=cal_count(edged, 0, 327, 241, 457)
    print(slot_3)

    #cv2.rectangle(edges, (415, 230), (630, 410), (255,0,0), 2)
    slot_4=cal_count(edged, 436, 39, 637, 143)
    print(slot_4)

    #cv2.rectangle(edges, (415, 230), (630, 410), (255,0,0), 2)
    slot_5=cal_count(edged, 440, 182, 637, 290)
    print(slot_5)

    #cv2.rectangle(edges, (415, 230), (630, 410), (255,0,0), 2)
    slot_6=cal_count(edged, 453, 330, 631, 453)
    print(slot_6)
    #store the values in a table named slots
    slots = [slot_1,slot_2,slot_3,slot_4,slot_5,slot_6]
    
    #compare each edges's value with our sure-edge "seuil" 
    for s in slots:
        if s > 600:
            slots[slots.index(s)] = "Not Available"
        else:
            slots[slots.index(s)] = "Available"
    return slots




#-----------------------send_slot info------------------------------------------
def send_txt(chat_id, msg):
    bot.sendMessage(chat_id, msg)

#-----------------------send_slot_photo----------------------------------------
def send_photo(chat_id, photo, caption=None):
    with open(photo, mode="r") as f:
        bot.sendPhoto(chat_id,f, caption)

#-------------------------input msg handle loop -------------------------------
def handle(msg):
    #print msg
    try:
        date = msg['date']
        usr_name = msg['from']['first_name']
        chat_id = msg['chat']['id']
        msg_id = msg['message_id']
        command = msg['text']
    except:
        print("Unexpected msg")
        pass
    else:
        print ('Got command: %s' % command)
        #the cmd photo take a current picture to our Parking
        if command == "photo":
            try:
                capture_img()
            except:
                print ("fail to capture Image")
            else:
                send_photo(chat_id, "process_img.png")
        #take the current picture and analyse it 
        #return the status of all the places  
        if command == "slots":
            try:
                capture_img()
                time.sleep(1)
                slots = solt_info()
            except:
                print("Fail to send slots info")
            else:
                msg = "Parking Slots : \n" +"Slot-1: "+slots[0]+"\n" + "Slot-2: "+slots[1]+"\n"+ "Slot-3: "+slots[2]+"\n"+ "Slot-4: "+slots[3]+"\n"+ "Slot-5: "+slots[4]+"\n"+ "Slot-6: "+slots[5]
                send_txt(chat_id, msg)
        #take the current picture and analyse it 
        #return the available places
        if command == "available slots":
            try:
                capture_img()
                time.sleep(1)
                slots = solt_info()
            except:
                print("Fail to send slots info")
            else:
                msg = "Available Slots \n"

                for s_no, s in enumerate(slots, start=1):
                    count=0
                    if s == "Available":
                        msg +="slot: "+ str(s_no) +"\n"
                        count+=1
                if count == 0:
                    msg = "Parking Full"

                send_txt(chat_id, msg)
                        #commands(chat_id, msg_id, date, command, usr_name, first_name, last_name)








#-------------------------Digi-server-bot config -------------------------------
#Connect to the app "Telegram" with the following token (which is giving by the application)
bot = telepot.Bot('1065536248:AAFGRB3QTB3QCDM6G5cNwhc3DS8wCA_BuWI')##954716912:AAHWXjc4lMmBBS3NR9woV7xc5EpT-mKV5gE
bot.message_loop(handle)
#the process is waiting for a cmd (commande line : slots | availabe slots)
print ('I am listening...')

while 1:
    time.sleep(1)