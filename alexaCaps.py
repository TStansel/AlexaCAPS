from selenium import webdriver 
import time

# Taking input from user 
search_string = "Harvard+Counseling+and+Psychological+Services"

# This is done to structure the string 
# into search url.(This can be ignored) 
search_string = search_string.replace(' ', '+') 


browser = webdriver.Chrome() 


matched_elements = browser.get("https://www.google.com/search?q=" +search_string) 
time.sleep(3)
results = browser.find_element_by_tag_name('h3')


