import requests
import time
from selenium import webdriver
import uuid
import requests
import sys

def main():
    args=sys.argv
    target_word=args[1]
    target_num=int(args[2])
    #------------------------------------start scraping-------------------------------------------------
    browser_object=TargetBrowser(target_word,target_num)
    browser_object.open_target_page()
    browser_object.get_img_url()

#-----------------------------------------class----------------------------------------------------------
class TargetBrowser:
    def __init__(self,target_string,scraping_num):
        self.target_string=target_string
        self.scraping_num=scraping_num
        
        #use site url
        self.url = "https://images.search.yahoo.com"
        #chromedriver path
        self.chromedriver_path="../chromedriver.exe"
        
        
        self.browser=webdriver.Chrome(executable_path=self.chromedriver_path)
        
    def open_target_page(self):
        
        self.browser.get(self.url)
        
        self.search_text_element=self.browser.find_element_by_id("yschsp")
        self.search_text_submit_element=self.browser.find_element_by_class_name("ygbt")
        
        self.search_text_element.send_keys(self.target_string)
        self.search_text_submit_element.click()
        time.sleep(5)
    
    def get_img_url(self):
        self.page_down_func();
        images_count_flug=False
        
        self.images_list=[]
        self.images_element=self.browser.find_elements_by_css_selector("li a.img img")
        
        self.show_more_button=self.browser.find_element_by_name("more-res")
        
        #get element
        while(not images_count_flug):
            if len(self.images_element)>self.scraping_num:
                images_count_flug=not images_count_flug
            else:
                try:
                    self.page_down_func()
                    #self.show_more_button.click()
                    self.images_element=self.browser.find_elements_by_css_selector("li a.img img")
                except:
                    images_count_flug=not images_count_flug
        #get all element--------------------------------------------------------
        
        self.page_down_func()
        self.images_element=self.browser.find_elements_by_css_selector("li a.img img")
        
        #delete None
        for img in self.images_element:
            if img.get_attribute("src") == None:
                continue
            else:
                self.images_list.append(img.get_attribute("src"))
                self.save_images(img.get_attribute("src"))
        print(len(self.images_list))
        
        
    def page_down_func(self):
            self.browser.find_element_by_tag_name('body').click()
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(5)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            
    def save_images(self,src):
        print(src,"-------------------------------------------------")
        response=requests.get(src)
        image=response.content
        
        with open(str("../get_images_folder/")+str(self.target_string)+str(uuid.uuid4())+str(".jpg"),"wb") as f:
            f.write(image)
if __name__ == "__main__":
    main()
