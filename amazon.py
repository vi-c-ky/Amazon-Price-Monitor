import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
import os
import datetime

marketIds = []# Market IDs of competitors to moniter
#file = open("ids.txt", "r")
#csv_reader = csv.reader(file, delimiter=',')
#for row in csv_reader:
#    marketIds.append(row[0])
#file.close()


def getData():
    global f,f_writer,browser
    opts = Options() #Creats option object
    browser = Chrome(options=opts) #Creates browser with options
    f = open("stock.txt", "w",newline='')
    f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #for each brand
    getPageData()
    f.close()
            
def writeData(ID):
    #for each product
    for i in range(len(prices)):
        f_writer.writerow([names[i].get_attribute("innerHTML"),prices[i].get_attribute("innerHTML"), marketIds[ID]])       
        #print(prices[i].get_attribute("innerHTML"))
        #print(names[i].get_attribute("innerHTML"))
    

    
def getPageData():
    global prices,names,Pageprices,pageNames, pageID
    Pageprices =[]
    pageNames =[]
    pageID = []
    for ids in range(len(marketIds)):
        browser.get('https://www.amazon.co.uk/s?me=%s' %marketIds[ids]) #Browser goes to site
        totalPages = browser.find_elements_by_class_name('a-disabled')[2].text
        print(totalPages)
        #for each page
        for page in range(int(totalPages)):
            browser.get('https://www.amazon.co.uk/s?me={}&page={}'.format(marketIds[ids],page+1))
            time.sleep(1)
            pageNum = browser.find_element_by_xpath('.//a[@aria-current="page"]')
            #print(pageNum.get_attribute("innerHTML"))
            prices = browser.find_elements_by_xpath('.//span[@class = "a-offscreen"]')
            time.sleep(1)
            names = browser.find_elements_by_xpath('.//span[@class = "a-size-medium a-color-base a-text-normal"]')
            time.sleep(1)
            
            delete = []
            for i in range(len(prices)):
                #print(i,len(prices))
                parentElement = prices[i].find_element_by_xpath('..')
                if parentElement.get_attribute("data-a-color") == "secondary":
                    delete.append(prices[i])
            
            for num in range(len(delete)):
                prices.remove(delete[num])
                  
            for i in range(len(prices)):
                Pageprices.append(prices[i].get_attribute("innerHTML"))
                pageNames.append(names[i].get_attribute("innerHTML"))
                pageID.append(marketIds[ids])
            writeData(ids)
        print(Pageprices)
        
            

def compareData():
    getData()
    print(len(readPrice))
    print(len(Pageprices))
    x = datetime.datetime.now()
    if(os.path.exists("{} {} {}.txt".format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b"))) == True):
        os.remove("{} {} {}.txt".format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b")))
    file = open("{} {} {}.txt".format(x.strftime("%a"),x.strftime("%d"),x.strftime("%b")), "w")
    for i in range(len(Pageprices)):
    
        if readPrice[i] != Pageprices[i] and pageID[i] == readID[i] and pageNames[i] == readNames[i]:
            file.write("{},{},{},{}\n".format(pageNames[i], readPrice[i],Pageprices[i],readID[i]))
        
        
            
    file.close()      

def readData():
     global readNames, readPrice, readID
     readNames = []
     readPrice =[]
     readID = []
     file = open("stock.txt", "r")
     csv_reader = csv.reader(file, delimiter=',')
     for row in csv_reader:
        readNames.append(row[0])
        readPrice.append(row[1])
        readID.append(row[2])
     file.close()
     os.remove("stock.txt")
     
     compareData()
        #print(f'\t{row[0]} {row[1]} {row[2]}')


if (os.path.exists("stock.txt") != True):
    getData()
    f.close()
else:
    readData()
#enterBox = browser.find_element_by_name('q')
#enterBox.click() aria-current="page" a-size-medium a-color-base a-text-normal
#data-a-color a-offscreen
