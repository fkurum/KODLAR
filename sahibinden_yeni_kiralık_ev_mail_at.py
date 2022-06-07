#!/usr/bin/env python
# coding: utf-8

# In[25]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

pd.options.mode.chained_assignment = None  # default='warn'


# In[26]:


tumliste=[]
farkliliste=[]
driver = webdriver.Chrome(ChromeDriverManager().install())


# In[27]:


def check(dff_list,dfk_list):
    linklist = []
    site ='https://www.sahibinden.com/kiralik-daire?pagingSize=50&a812=40728&a812=40602&a812=40603&a812=40604&a812=40605&a812=40606&a812=40607&a812=43901&a812=43902&sorting=date_desc&a811=40592&a811=40593&a811=40594&a811=40595&a811=40596&a811=40597&a811=40598&a811=40599&a811=40600&price_min=3000.0&address_town=450&address_town=430&address_town=431&address_town=432&address_town=433&address_town=422&address_town=435&address_town=436&address_town=425&address_town=416&address_town=417&address_town=428&address_town=429&price_max=4200.0&address_city=34'
    stop=1
    #birkaç sayfa yapmak istersek diye döngü burada sayfa adedi değiştirilebilir
    bakilacak_sayfa_adedi=1

    for i in range(1,bakilacak_sayfa_adedi+1):

        driver.get(site)
        time.sleep(3)
        driver.get(site)
        #sahibinden beni blokladı sayfayı yenileyince açılıyor

        for x in range(1,52):
            if x == 4: #reklam
                continue
            try:
                val_l ='//*[@id="searchResultsTable"]/tbody/tr[{}]/td[2]/a'.format(x)

                link = driver.find_element(By.XPATH,value=val_l).get_attribute('href')



            except:
                print('HATA!!!')
                continue
            else:
                linklist.append(link)
                
        site ="https://www.sahibinden.com/kiralik-daire?pagingOffset={}&pagingSize=50&a812=40728&a812=40602&a812=40603&a812=40604&a812=40605&a812=40606&a812=40607&a812=43901&a812=43902&sorting=date_desc&a811=40592&a811=40593&a811=40594&a811=40595&a811=40596&a811=40597&a811=40598&a811=40599&a811=40600&price_min=3000.0&address_town=450&address_town=430&address_town=431&address_town=432&address_town=433&address_town=422&address_town=435&address_town=436&address_town=425&address_town=416&address_town=417&address_town=428&address_town=429&price_max=4200.0&address_city=34".format(i*50)
    for i in linklist:
        if i in dff_list:
            None
        else:
            dff_list.append(i)
            dfk_list.append(i)   
    if len(dfk_list) <1:
        dfk_list = []
    else:
        olumlumail(dfk_list)
        dfk_list= []
        print("mail gönderildi.")

    return dff_list,dfk_list


# In[ ]:





# In[30]:


def olumlumail(dfk_list): 
    new_list = []
    tutucu = 1
    dongu = len(dfk_list)
    if dongu > 48:
        dongu = 48
    
    for x in range(0,dongu):
        if tutucu ==1 :
            new_list = str(x) +' '+ str(dfk_list[x]) +  ' </br> '
            tutucu = 0
        else:
            new_list =   str(new_list) +str(x) +' '+ str(dfk_list[x]) +  ' </br> '
    
    mail = smtplib.SMTP("smtp.gmail.com",587)          
    mail.ehlo()
    mail.starttls()
    mail.login("furkankurum23@gmail.com", "x")
    mesaj = MIMEMultipart()

    mesaj["From"] = "furkankurum23@gmail.com"        # Gönderen kişi
    mesaj["To"] = "furkankurum23@gmail.com"          # Alıcı

    mesaj["Subject"] = "SAHİBİNDEN LİNKLER"  # Konu

    body = new_list

    body_text = MIMEText(body, "html")  
    mesaj.attach(body_text)
    mail.sendmail( mesaj["From"], mesaj["To"], mesaj.as_string())


# In[31]:


flag=0
if (flag==0):
    tumliste,farkliliste = check(tumliste,farkliliste)
    time.sleep(2)
    flag=1
while(flag!=0):
    tumliste,farkliliste = check(tumliste,farkliliste)
    time.sleep(2)


# In[ ]:




