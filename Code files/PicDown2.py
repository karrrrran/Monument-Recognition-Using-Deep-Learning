from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import urllib2

searchterm = raw_input("Enter the name of the picture to download:") 
url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
browser = webdriver.Firefox() # instantiate Firefox webriver
browser.get(url) # open the web browser
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
counter = 0
succounter = 0

if not os.path.exists(searchterm):  #create a seperate directory for each image
    os.mkdir(searchterm)

for _ in range(500):
    browser.execute_script("window.scrollBy(0,10000)") #selenium based web page scroller

for x in browser.find_elements_by_xpath("//div[@class='rg_meta']"):  #to find the image in the webpage
    counter = counter + 1
    print "Total Count:", counter
    print "Succsessful Count:", succounter
    print "URL:",json.loads(x.get_attribute('innerHTML'))["ou"]  #Gets the url of the actual location of image 

    img = json.loads(x.get_attribute('innerHTML'))["ou"] 
    imgtype = json.loads(x.get_attribute('innerHTML'))["ity"] 
    try: # This block will retreive the url of the image from GImages and using files first read the image and then write it into the directory
        req = urllib2.Request(img, headers={'User-Agent': header})
        raw_img = urllib2.urlopen(req).read()
        File = open(os.path.join(searchterm , searchterm + "_" + str(counter) + "." + imgtype), "wb") # ex : CST_6.jpg
        File.write(raw_img)
        File.close()
        succounter = succounter + 1
    except:
            print "can't get the image"

print succounter, "Pictures succesfully downloaded"
browser.close()