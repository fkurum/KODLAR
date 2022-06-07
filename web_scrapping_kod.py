#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import date, timedelta
pd.options.mode.chained_assignment = None  # default='warn'
import re


# In[ ]:


driver = webdriver.Chrome(ChromeDriverManager().install())

# İLLERİN LİNKİNİ ÇEKME 
driver.get("https://www.zingat.com/bolge-raporu")
link = driver.find_elements(by = By.CLASS_NAME, value = 'indicator')
linklist = []
for x in link:
    linklist.append(x.get_attribute("href"))
illink = pd.DataFrame (linklist,columns = ["IL_LINK"])

# İLCELERİN LİNKİNİ CEKME
linklist = []
for x in illink.IL_LINK:
    driver.get(x)
    link = driver.find_elements(by = By.CLASS_NAME, value = 'indicator')
    for t in link:
        linklist.append([x,t.get_attribute("href")])
        
# MAHALLE LİNKİNİ CEKME
linklist = []
for x in linkler.ILCE_LINK:
    driver.get(x)
    link = driver.find_elements(by = By.CLASS_NAME, value = 'indicator')
    for t in link:
        linklist.append([x,t.get_attribute("href")])
yeniframe = pd.DataFrame(linklist,columns = ["ILCE_LINK","MAHALLE_LINK"])
linkler = linkler.merge(yeniframe,on = "ILCE_LINK")
linkler.to_csv("zingat_link.csv",header = True , index = False)

#DEMOGRAFIK LINKLERI TOPLAMA
linkler["IL_DEMOGRAFIK"] = np.nan
linkler["ILCE_DEMOGRAFIK"] = np.nan
linkler["MAHALLE_DEMOGRAFIK"] = np.nan
for x in linkler.IL_LINK:
    linkler.IL_DEMOGRAFIK[linkler.IL_LINK == x] = x +'?mode=demographics'
    
# In[ ]:


linkler = pd.read_csv("zingat_tum_linkler.csv")


# In[ ]:


counter = 0
p=0


# In[ ]:


kolonlar = ["ILCE_LINKI","ORTALAMA_SATIS","MINIMUM_SATIS","MAX_SATIS","GERI_DONUS_SURESI",
            "AYLIK_SATIS_FIYATI_DEGISIMI","UC_YILLIK_SATIS_DEGISIM","5_YILLIK_SATIS_DEGISIM",
            "KIRA_ORTALAMA","KIRA_MIN","KIRA_MAX","GERI_DONUS_SURESI","AYLIK_KIRA_DEGISIM",
            "UC_YILLIK_KIRA_DEGISIM","BES_YILLIK_KIRA_DEGISIM","TOPLAM_NUFUS","YILLIK_NUFUS_ARTISI",
            "SOSYO_EKONOMIK_DURUM","0-14","15-24","25-34","35,44","45-54","55-64","65+",
            "ESI_OLMUS","BOSANMIS","EVLI","BEKAR","OGRENIM_GORMEMIS","ILKOKUL",
            "ORTAOKUL","LISE","UNIVERSITE"]


# In[ ]:


counter = 0
p=0


# In[ ]:


liste = linkler.ILCE_LINK.unique()


# In[ ]:


for link in range(counter,len(liste)):
    bilgilerliste = []
    istekurl = []
    istektam = []
    driver.get(liste[link])

    piyasabilgileri = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[3]/div/div/div/div/div[2]/div[2]").text
    satisbilgileri = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[4]/div/div/div/div[1]/div").text
    time.sleep(5)
    try:
        driver.find_element(by = By.XPATH,value = "//*[@id='location-report']/div/section[3]/div/div/div/div/div[2]/div[1]/ul/li[2]").click()
    except:
        driver.find_element(by = By.XPATH,value = "//*[@id='location-report']/div/section[4]/div/div/div/div/div[2]/div[1]/ul/li[2]").click()
    try:
        piyasabilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[3]/div/div/div/div/div[2]/div[3]/ul").text
    except:
        piyasabilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[4]/div/div/div/div/div[2]/div[2]/ul/li[1]").text
    try:
        satisbilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[4]/div/div/div/div[2]/div").text
    except:
        satisbilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[5]/div/div/div/div[1]").text

    del driver.requests
    
    time.sleep(0.5)
    driver.get(liste[link]+'?mode=demographics')

    demografikbilgi = driver.find_element(by = By.XPATH , value='//*[@id="location-report"]/div/section[3]/div/div/div/div').text
    time.sleep(10)
    for request in driver.requests:
        if request.response:
            istekurl.append(request.url)
            istektam.append(request.url)
            istektam.append(request.response)
    egitim=None;evlilik=None;yas=None;
    b=0
    for x in istekurl:
        if evlilik==None:
            evlilik = re.search("type=population-by-marital-status&locationId=*",x)
            b=b+1
        else:
            api1 = istekurl[b-1]
    b=0
    for x in istekurl:
        if egitim==None:
            egitim = re.search("type=population-by-education&locationId=*",x)
            b=b+1
        else:
            api2 = istekurl[b-1]
    b=0
    for x in istekurl:
        if yas==None:
            yas = re.search("type=population-by-age&locationId=*",x)
            b=b+1
        else:
            api3 = istekurl[b-1]
        
    evlilik       = istektam.index(api1);evlilik = evlilik+1
    egitim        = istektam.index(api2);egitim = egitim+1
    yas           = istektam.index(api3);yas = yas+1
    yasbilgi1     = istektam[yas].body.decode().split(',')[1].split(':')[2] #0-14
    yasbilgi2     = istektam[yas].body.decode().split(',')[2].split(':')[1] #15-24
    yasbilgi3     = istektam[yas].body.decode().split(',')[3].split(':')[1] #25-34
    yasbilgi4     = istektam[yas].body.decode().split(',')[4].split(':')[1] #35-44
    yasbilgi5     = istektam[yas].body.decode().split(',')[5].split(':')[1] #45-54
    yasbilgi6     = istektam[yas].body.decode().split(',')[6].split(':')[1] #55-64
    yasbilgi7     = istektam[yas].body.decode().split(',')[7].split(':')[1].split('}')[0] #65+
#########################################################################################################################
    
    if re.search('Eşi Ölmüş',istektam[evlilik].body.decode().split(',')[1].split(':')[1]) != None:
        evlilikbilgi1 = istektam[evlilik].body.decode().split(',')[1].split(':')[2] #eşi ölmüş
    elif re.search('Eşi Ölmüş',istektam[evlilik].body.decode().split(',')[2].split(':')[0]) != None:
        evlilikbilgi1 = istektam[evlilik].body.decode().split(',')[2].split(':')[1] 
    elif re.search('Eşi Ölmüş',istektam[evlilik].body.decode().split(',')[3].split(':')[0]) != None:
        evlilikbilgi1 = istektam[evlilik].body.decode().split(',')[3].split(':')[1]
    else:
        evlilikbilgi1 = istektam[evlilik].body.decode().split(',')[4].split(':')[1].split('}')[0]
        
#########################################################################################################################
 
    if re.search("Boşanmış",istektam[evlilik].body.decode().split(',')[2].split(':')[0]) !=None:
        evlilikbilgi2 = istektam[evlilik].body.decode().split(',')[2].split(':')[1] #boşanmış
    elif re.search("Boşanmış",istektam[evlilik].body.decode().split(',')[1].split(':')[1]) !=None:
        evlilikbilgi2 = istektam[evlilik].body.decode().split(',')[1].split(':')[2]
    elif re.search("Boşanmış",istektam[evlilik].body.decode().split(',')[3].split(':')[0]) !=None:    
        evlilikbilgi2 = istektam[evlilik].body.decode().split(',')[3].split(':')[1]
    else: 
        evlilikbilgi2 = istektam[evlilik].body.decode().split(',')[4].split(':')[1].split('}')[0] #bekar

#########################################################################################################################
   
    if re.search("Evli",istektam[evlilik].body.decode().split(',')[3].split(':')[0]) !=None:
        evlilikbilgi3 = istektam[evlilik].body.decode().split(',')[3].split(':')[1]
    elif re.search("Evli",istektam[evlilik].body.decode().split(',')[1].split(':')[1]) !=None:
        evlilikbilgi3 = istektam[evlilik].body.decode().split(',')[1].split(':')[2]
    elif re.search("Evli",istektam[evlilik].body.decode().split(',')[2].split(':')[0]) !=None:
        evlilikbilgi3 = istektam[evlilik].body.decode().split(',')[2].split(':')[1]
    else:
        evlilikbilgi3 = istektam[evlilik].body.decode().split(',')[4].split(':')[1].split('}')[0]
        
#########################################################################################################################
 
    if re.search("Bekar",istektam[evlilik].body.decode().split(',')[3].split(':')[0]) !=None:
         evlilikbilgi4 = istektam[evlilik].body.decode().split(',')[3].split(':')[1]
    elif re.search("Bekar",istektam[evlilik].body.decode().split(',')[1].split(':')[1]) !=None:
        evlilikbilgi4 = istektam[evlilik].body.decode().split(',')[1].split(':')[2]
    elif re.search("Bekar",istektam[evlilik].body.decode().split(',')[2].split(':')[0]) !=None:
        evlilikbilgi4 = istektam[evlilik].body.decode().split(',')[2].split(':')[1]
    else:
        evlilikbilgi4 = istektam[evlilik].body.decode().split(',')[4].split(':')[1].split('}')[0]
        
#########################################################################################################################

    egitim1       = istektam[egitim].body.decode().split(',')[1].split(':')[2] #ögrenim görmemis
    egitim2       = istektam[egitim].body.decode().split(',')[2].split(':')[1] #ilkokul
    egitim3       = istektam[egitim].body.decode().split(',')[3].split(':')[1] #ortaokul
    egitim4       = istektam[egitim].body.decode().split(',')[4].split(':')[1] #lise
    egitim5       = istektam[egitim].body.decode().split(',')[5].split(':')[1].split('}')[0] #üniversite
    try:
        bilgilerliste.append([liste[link],piyasabilgileri.split("\n")[1],piyasabilgileri.split("\n")[2],
                              piyasabilgileri.split("\n")[4],piyasabilgileri.split("\n")[7],
                              satisbilgileri.split("\n")[0],satisbilgileri.split("\n")[2],
                              satisbilgileri.split("\n")[4],piyasabilgilerikira.split("\n")[1],
                              piyasabilgilerikira.split("\n")[2],piyasabilgilerikira.split("\n")[4],
                              piyasabilgilerikira.split("\n")[7],satisbilgilerikira.split("\n")[0],
                              satisbilgilerikira.split("\n")[2],satisbilgilerikira.split("\n")[4],
                              demografikbilgi.split("\n")[4],demografikbilgi.split("\n")[5].split(":")[1],
                              demografikbilgi.split("\n")[7],yasbilgi1,yasbilgi2,yasbilgi3,yasbilgi4,
                              yasbilgi5,yasbilgi6,yasbilgi7,evlilikbilgi1,evlilikbilgi2,evlilikbilgi3,evlilikbilgi4,
                              egitim1,egitim2,egitim3,egitim4,egitim5])
    except:
            driver.get(liste[link])
            piyasabilgileri = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[4]/div/div/div/div/div[2]/div[2]/ul").text
            satisbilgileri = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[5]/div/div/div/div[1]").text
            time.sleep(4.5)
            driver.find_element(by = By.XPATH,value = "//*[@id='location-report']/div/section[4]/div/div/div/div/div[2]/div[1]/ul/li[2]").click()
            piyasabilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[4]/div/div/div/div/div[2]/div[3]/ul").text
            satisbilgilerikira = driver.find_element(by = By.XPATH , value = "//*[@id='location-report']/div/section[5]/div/div/div/div[2]/div").text
            driver.get(liste[link]+'?mode=demographics')
            demografikbilgi = driver.find_element(by = By.XPATH , value='//*[@id="location-report"]/div/section[4]/div/div/div/div').text

            bilgilerliste.append([liste[link],piyasabilgileri.split("\n")[1],piyasabilgileri.split("\n")[2],
                              piyasabilgileri.split("\n")[4],piyasabilgileri.split("\n")[7],
                              satisbilgileri.split("\n")[1],satisbilgileri.split("\n")[3],
                              satisbilgileri.split("\n")[5],piyasabilgilerikira.split("\n")[1],
                              piyasabilgilerikira.split("\n")[2],piyasabilgilerikira.split("\n")[4],
                              piyasabilgilerikira.split("\n")[7],satisbilgilerikira.split("\n")[0],
                              satisbilgilerikira.split("\n")[2],satisbilgilerikira.split("\n")[4],
                              demografikbilgi.split("\n")[4],demografikbilgi.split("\n")[5].split(":")[1],
                              demografikbilgi.split("\n")[7],yasbilgi1,yasbilgi2,yasbilgi3,yasbilgi4,
                              yasbilgi5,yasbilgi6,yasbilgi7,evlilikbilgi1,evlilikbilgi2,evlilikbilgi3,evlilikbilgi4,
                              egitim1,egitim2,egitim3,egitim4,egitim5])
            
    zingat = pd.DataFrame(bilgilerliste,columns = kolonlar)
    if p==0:
        zingat.to_csv("zingat_ilce_bazinda_bilgiler.csv",index = False,mode = 'a',header = True)
        p=p+1
    else:
        zingat.to_csv("zingat_ilce_bazinda_bilgiler.csv",index = False,mode = 'a',header = False)
    print(counter,liste[link])
    counter=counter+1


# In[ ]:





# In[ ]:





# In[ ]:




