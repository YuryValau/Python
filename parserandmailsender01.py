import requests
import smtplib
import time
from bs4 import BeautifulSoup

attempts = 10000000
sleep = 10

url='http://forum.onliner.by/viewtopic.php?t=1128205&start=293200'
fromaddr = 'vyv553@gmail.com'
toaddrs  = 'vyv553@gmail.com'
username = 'vyv553@gmail.com'
password = 'valov001'

def sendmail(i,text):
   
    msg = 'Subject: {}\n\n{}'.format("Alert["+str(i)+"]", text)

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg.encode('utf-8').strip())
        server.quit()

        print('Email sent!'+ toaddrs)
    except Exception as e:
        print (e)
    print(str(i)+" attempts remain")

listBuff = []

while i < attempts:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    
    listNew = []
    for liTag in soup.find_all("li", {"class":"msgpost"}):
        for tag in liTag.find_all("div", {"class":"content"}):
            for aTag in tag.find_all('p'):
                listNew.append(aTag.text)

    sub=set(listNew)-set(listBuff)            
    if(sub!=set([])):
        string='\n'.join(sub)
        print(string)
        sendmail(i,string)            
    listBuff = listNew.copy()
    print("check "+str(i))
    time.sleep(sleep)
    i+=1