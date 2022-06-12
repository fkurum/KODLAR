#!/usr/bin/env python
# coding: utf-8
#Bitirme çalışması için yaptığımız uzaktan erişimli otonom silah. Sistemin arayüzü tkinter kütüphanesi üzerinden yazılmıştır.
# In[1]:
#

from IPython.display import clear_output
import socket
import sys
import cv2
import matplotlib.pyplot as plt
import pickle
import numpy as np
import struct
import zlib
from PIL import Image, ImageOps , ImageTk , Image
import mediapipe as mp
import time
import smtplib
import ssl

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
    


# In[2]:


def mailgonder():
    # Define the transport variables
    ctx = ssl.create_default_context()
    password = "x"    # Your app password goes here
    sender = "furkankurum23@gmail.com"    # Your e-mail address
    receiver = "furkankurum23@gmail.com" # Recipient's address

    # Create the message
    message = MIMEMultipart("mixed")
    message["Subject"] = "OTONOM SİLAH"
    message["From"] = sender
    message["To"] = receiver

    # Mesaj ekleme
    message.attach(MIMEText("İnsan Tespiti Yapıldı", "plain"))

    # Fotoğraf Ekleme
    filename = r'C:\Users\HP\Desktop\otonom/mail.jpg'
    with open(filename, "rb") as f:
        file = MIMEApplication(f.read())
    disposition = f"attachment; filename={filename}"
    file.add_header("Content-Disposition", disposition)
    message.attach(file)

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
    label = Label( entry, text = 'İnsan tespit edildi.')
    label.pack()
    root.update()
    label = Label( entry, text = 'Mail gönderildi.')
    label.pack()
    root.update()

    


# In[3]:


def baglanti_kur():    
    global conn
    HOST='192.168.137.1'
    PORT=12345

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    label = Label( entry, text = 'Soket oluşturuldu.')
    label.pack()
    root.update()
    s.bind((HOST,PORT))
    label = Label( entry, text = 'Socket bind complete')
    label.pack()
    root.update()
    s.listen(10)
    label = Label( entry, text = 'Socket dinleniyor.')
    label.pack()
    root.update()
    conn,addr=s.accept()
    label = Label( entry, text = 'Bağlantı başarıyla başlatıldı.')
    label.pack()
    root.update()
    label = Label( entry, text = '3sn sonra mod seçebilirsiniz.')
    label.pack()
    root.update()


# In[4]:


def baglantiyi_baslat():
    global H
    global mail
    H = True
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    positionx = 90
    positiony = 90
    data = b""
    payload_size = struct.calcsize(">L")
    flag= 0
    label = Label( entry, text = 'Otonom sistem başlatıldı.')
    label.pack()
    root.update()
    while(H):
        while len(data) < payload_size:
            data += conn.recv(4096)
        # cleint socket inden görüntü alma
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        # resmi açılacak şekilde ayarlama 
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        #buraya goruntu isleme algoritmaları eklenecek daha sonra positionx ve positiony degerleri gonderilecek
        lmlist = []
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        
        results = pose.process(imgRGB)
        #print(results.pose_landmarks)
        if results.pose_landmarks:
            if mail:
                cv2.imwrite(r'C:\Users\HP\Desktop\otonom/mail.jpg', frame) 
                mailgonder()
                mail_sistemini_kapat()
            #mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #tüm noktaları çizdirmek istersek
            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = frame.shape    #(240,320,3)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                #print(lmlist[0][1]) #x koordinatlarıd
                #print(lmlist[0][2]) #y koordinatları
                cv2.circle(frame, (lmlist[0][1], lmlist[0][2]), 5, (255, 0, 0), cv2.FILLED)
            arayuz = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgara = ImageTk.PhotoImage(Image.fromarray(arayuz))
            L1["image"] =imgara
            root.update()
            liste = str(positionx) + '\n' + str(positiony)
            conn.sendto(liste.encode(),('192.168.137.1',12345))

             # ---------------------------------------- #
            if lmlist[0][1] < 120:
                positionx = positionx - 5
                #print("sola don")
                if positionx <= 10:
                    positionx = 90
                    time.sleep(0.220)
            else:
                positionx = positionx + 5
                #print("saga don")
                if positionx >= 170:
                    positionx = 90
                    time.sleep(0.220)
#     ---------------------------------------- #
#             if lmlist[0][2] < 160:
#                 positiony = positiony - 5
#                 print("asagi in")
#                 if positiony <= 10:
#                     positiony = 90
#                     time.sleep(0.020)
#             else:
#                 positiony = positiony + 5
#                 print("yukari cik")
#                 if positiony >= 175:
#                     positiony = 90
#                     time.sleep(0.020)        
        else:
            arayuz = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imgara = ImageTk.PhotoImage(Image.fromarray(arayuz))
            L1["image"] =imgara
            root.update()
            if flag%2==0:
                positionx=positionx+5
                time.sleep(0.04)
                if positionx>170:
                    flag = flag+1
            if flag%2==1:
                positionx=positionx-5
                time.sleep(0.04)
                if positionx < 10:
                    flag = flag+1
                
        
            liste = str(positionx) + '\n' + str(positiony)
            conn.sendto(liste.encode(),('192.168.137.1',12345))


# In[5]:


def manuel():
    global manuel
    manuel = True
    root.update()
    data = b""
    payload_size = struct.calcsize(">L")
    label = Label( entry, text = 'Manuel sistem başlatıldı.')
    label.pack()
    root.update()
    while manuel:
        while len(data) < payload_size:
            data += conn.recv(4096)
        # cleint socket inden görüntü alma
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        lmlist = []
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imgara = ImageTk.PhotoImage(Image.fromarray(imgRGB))
        L1["image"] =imgara
        root.update()
        positionx = int(scale.get())
        positiony = int(scale2.get())
        liste = str(positionx) + '\n' + str(positiony)
        conn.sendto(liste.encode(),('192.168.137.1',12345))
        
        


# In[6]:


def otonom_sistemi_kapat():
    global H
    H = False
    label = Label( entry, text = 'Otonom sistem durduruldu.')
    label.pack()
    root.update()
def manuel_sistemi_kapat():
    global manuel
    manuel = False
    label = Label( entry, text = 'Manuel sistem durduruldu.')
    label.pack()
    root.update()
def baglantiyi_sifirla():
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()
    label = Label( entry, text = 'Bağlantı sıfırlandı.')
    label.pack()
    root.update()
def mail_sistemini_ac():
    global mail
    mail = True
    label = Label( entry, text = 'Mail gönderimi aktif.')
    label.pack()
    root.update()
def mail_sistemini_kapat():
    global mail
    mail = False
    label = Label( entry, text = 'Mail gönderimi devre dışı.')
    label.pack()
    root.update()


# In[7]:


import tkinter as tk
from tkinter import ttk,Scale,LabelFrame,Label

root = tk.Tk()
root.title('OTONOM SİLAH ARAYÜZ')
window_height = 530
window_width = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
style = ttk.Style(root)
root.tk.call('source', r"C:\Users\HP\Downloads\Azure-ttk-theme-main\azure dark\azure dark.tcl")
style.theme_use('azure')



frame1 = ttk.LabelFrame(root, text='Bağlantıyı Başlat', width=210, height=120)
frame1.place(x=20, y=12)
button1 = ttk.Button(frame1, text='Bağlantıyı Başlat ', command=baglanti_kur)
button1.place(x=20, y=18)
button2 = ttk.Button(frame1, text='Bağlantıyı Sıfırla', command=baglantiyi_sifirla)
button2.place(x=20, y=58)

sep1 = ttk.Separator()
sep1.place(x=20, y=150, width=210)

frame2 = ttk.LabelFrame(root, text='Manuel Sistemi Başlat', width=210, height=160)
frame2.place(x=20, y=160)
check1 = ttk.Button(frame2, text='Manuel Kontrol Et',command = manuel)
check1.place(x=20, y=18)
button4 = ttk.Button(frame2, text='Manuel Sistemi Kapat', command=manuel_sistemi_kapat)
button4.place(x=20, y=58)
scale = ttk.Scale(frame2, from_=0, to=180)
scale.place(x=25, y=95)
scale2 = ttk.Scale(frame2, from_=0, to=180)
scale2.place(x=25, y=118)


sep2 = ttk.Separator()
sep2.place(x=20, y=340, width=210)

frame3 = ttk.LabelFrame(root, text='Otonom Sistemi Başlat', width=210, height=120)
frame3.place(x=20, y=350)
button5 = ttk.Button(frame3, text='Otonom Kontrol Et ', command=baglantiyi_baslat)
button5.place(x=20, y=18)
button6 = ttk.Button(frame3, text='Otonom Sistemi Kapat', command=otonom_sistemi_kapat)
button6.place(x=20, y=58)


entry = ttk.LabelFrame(root,text = "LOG",width = 160,height =458)
entry.place(x=250, y=12)
treeScroll = ttk.Scrollbar(entry)
treeScroll.place()



f1 = LabelFrame(root,text= "KAMERA",width=360, height=280)
f1.place(x=420, y=20)

L1 = Label(f1)
L1.place(x=15 ,y=7.5)

sep2 = ttk.Separator()
sep2.place(x=420, y=320, width=360)

frame5 = ttk.LabelFrame(root, text='Mail Sistemini Başlat', width=360, height=120)
frame5.place(x=420, y=335)
button5 = ttk.Button(frame5, text='Mail Sistemini Aç', command=mail_sistemini_ac)
button5.place(x=20, y=18)
button6 = ttk.Button(frame5, text='Mail Sistemini Kapat', command=mail_sistemini_kapat)
button6.place(x=20, y=58)


root.mainloop()


# In[ ]:





# In[ ]:




