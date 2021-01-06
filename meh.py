import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json

class Livreur:
    def __init__(self, Name, PhoneNum,WhatsappNum):
        self.Name = Name
        self.PhoneNum = PhoneNum
        self.WhatsappNum = WhatsappNum
        self.Cities = list()

def login():
    opt = webdriver.ChromeOptions()
    #opt.addgument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),  chrome_options=opt)
    driver.get("https://liv.ma/Login/")
    email = driver.find_element_by_name("email")
    email.send_keys("ayoub.assalo@gmail.com")
    pw = driver.find_element_by_name("password")
    pw.send_keys("156874239")
    btn = driver.find_element_by_name("login")
    btn.click()
    time.sleep(2)
    driver.get("https://liv.ma/Find-Delivery/")
    return driver

go = login()
try:
    while len(go.find_elements_by_class_name("loadMore")) == 1:
        go.find_elements_by_class_name("loadMore")[0].click()
        time.sleep(1)
except:
    print("meh")


profiles = go.find_elements_by_class_name("col-lg-3")

links = list()

for profile in profiles:
    links.append(profile.find_element_by_tag_name("a").get_attribute("href"))

data = list()
for link in links:
    go.get(link)
    time.sleep(2)
    try:
        name = go.find_elements_by_tag_name("h3")[0].get_attribute("innerHTML").strip(' \n')
        print(name)
        phone = go.find_elements_by_class_name("text-uppercase")[0].find_element_by_tag_name("a").get_attribute("innerHTML")
        print(phone)
        wsp = go.find_elements_by_class_name("text-uppercase")[1].get_attribute("innerHTML").strip(' ').split()[9]
        print(wsp)
    except:
        break
    user = Livreur(name,phone,wsp)
    try:
        num = int(go.find_elements_by_class_name("ml-3")[1].find_element_by_tag_name("b").get_attribute("innerHTML"))
        cts = go.find_elements_by_css_selector(".font-weight-bold.mb-3")
        for i in range(0,num):
            user.Cities.append(cts[i].get_attribute("innerHTML"))
    except:
        ct = go.find_elements_by_class_name("ml-3")[1].find_element_by_tag_name("b").get_attribute("innerHTML").strip(' \n')
        user.Cities.append(ct)
    print(user.Cities)
    data.append(user)
with open("/Users/moerradi/Desktop/liv_bot/data.json",'w',encoding='utf8') as file:
    json.dump([ob.__dict__ for ob in data],file,indent=4,ensure_ascii=False)