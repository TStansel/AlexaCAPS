from selenium import webdriver 
import time
import re

def lambda_handler(event,context):
    # Taking input from user 
    search_string = "harvard+Counseling+and+Psychological+Services"

    #Format the String if needed
    search_string = search_string.replace(' ', '+') 

    #Open Chrome
    browser = webdriver.Chrome() 

    #Go to the google search results
    matched_elements = browser.get("https://www.google.com/search?q=" +search_string) 
    time.sleep(3)

    #Get the first result and click it
    results = browser.find_element_by_tag_name('h3')
    results.click()

    #Get the pages HTMl and using regex get all possible phone numbers
    doc = browser.page_source
    phones = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4})',doc)

    #Do some more proofing to cut the numbers down
    proofedPhones = []
    for phone in phones:
        if phone.rfind("(") != -1:
            proofedPhones.append(phone)
        elif phone.rfind(".") != -1:
            proofedPhones.append(phone)



