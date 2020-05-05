import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
import urllib.request
import lxml

class Wallpaper_Scraper():

    def initialise(self, source_text):
        soup = BeautifulSoup(source_text,'lxml')
        heading = soup.find_all('h1')
        heading = heading[0].text
        pattern = re.compile('[^0-9]+')
        num = re.sub(pattern,'',heading)
        num = int(num)
        pages =np.ceil(num/24)
        return num, pages
    
    def get_images(self, source_text, dir_name, initial, final,text):
        c = 0
        soup = BeautifulSoup(source_text,'lxml')
        ids =  soup.find(id="thumbs")
        images = ids.findAll('li')
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'whatever')
        for img in images:
            url = img.find('img')['data-src']
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
        query = 'https://wallhaven.cc/search?q='+search_query
        r = requests.get(query)
        source_text = r.text
        num, pages = self.initialise(source_text)
        if num == 0:
            print('No image Found')
            return True
        dir_name = search_query.replace('_',' ')
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        initial = 0
        page_no = 3
        query = 'https://wallhaven.cc/search?q='+search_query
        if num < num_of_img:
            print('Sorry!!!\nWe have only', num,'images available with title',search_query)
        if num <= 48:
            initial = self.get_images(source_text, dir_name,initial, num_of_img,dir_name)
        else:
            initial = self.get_images(source_text, dir_name, initial, num_of_img,dir_name)
            while initial < num_of_img and page_no <= pages:
                query2 = query + '&page='+str(page_no)
                #print(query2)
                page_no += 1
                r = requests.get(query2)
                source_text = r.text
                initial = self.get_images(source_text, dir_name, initial, num_of_img,dir_name)
        return True