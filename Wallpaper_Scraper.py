import urllib.request
import webbrowser
from selenium import webdriver
import numpy  as np
from selenium.webdriver.chrome.options import Options
import os
import re


class Wallpaper_Scraper(object):

    def initselenium(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")

        chrome_driver = "chromedriver"
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
        return driver

    def initialise(self, driver):
        heading = driver.find_element_by_tag_name('h1').text
        pattern = re.compile('[^0-9]+')
        num = re.sub(pattern,'',heading)
        num = int(num)
        pages =np.ceil(num/24)
        return num, pages
    
    def get_images(self,driver, dir_name, initial, final,text):
        c = 0
        ids =  driver.find_element_by_id('thumbs')
        images = ids.find_elements_by_tag_name('li')
        #print(len(images),end="      ")
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'whatever')
        for img in images:
            url = img.find_element_by_tag_name("img").get_attribute('data-src')
            opener.retrieve(url, './'+dir_name+'/'+text+str(initial)+'.jpg')
            initial += 1
            c+=1
            if c == 24:
                break
            if final == initial:
                break
        return initial
    
    def wallpaper_scraper(self,search_query, num_of_img):
        search_query = search_query.replace('+',' ')
        driver = self.initselenium()
        query = 'https://wallhaven.cc/search?q='+search_query
        driver.get(query)
        num, pages = self.initialise(driver)
        if num == 0:
            print('No image Found')
            return True
        dir_name = search_query.replace('_',' ')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        initial = 0
        page_no = 3
        query = 'https://wallhaven.cc/search?q='+search_query
        driver.get(query)
        if num < num_of_img:
            print('Sorry!!!\nWe have only', num,'images available with title',search_query)
        if num <= 48:
            initial = self.get_images(driver, dir_name,initial, num_of_img,dir_name)
        else:
            initial = self.get_images(driver, dir_name, initial, num_of_img,dir_name)
            while initial < num_of_img and page_no <= pages:
                query2 = query + '&page='+str(page_no)
                #print(query2)
                page_no += 1
                driver.get(query2)
                initial = self.get_images(driver, dir_name, initial, num_of_img,dir_name)
        return True