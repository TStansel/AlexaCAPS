from selenium import webdriver 
import time
import re
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

class LaunchReqeustHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)
    
    def handle(self,handler_input):
        handler_input.response_builder.speak("Searching now.".set_should_end_session(False))
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self,handler_input,exception):
        return True
    def handle(self,handler_input,exception):
        print(exception)
        handler_input.response_builder.speak("Something went wrong. Please try again.")
        return handler_input.response_builder.response

class UniversityMHNumberIntentHandler(AbstractRequestHandler):
    def can_handle(self,handler_input):
        return is_intent_name("UniversityMHNumberIntent")(handler_input)
    
    def handle(self,handler_input):
        uni = handler_input.request_envelope.request.intent.slots['university'].value
        college = handler_input.request_envelope.request.intent.slots['college'].value
        if uni == None:
            uni = college
        phones = findNumber(uni)
        speech_text = phones[0]
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchReqeustHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(UniversityMHNumberIntentHandler())


def lambda_handler(event,context):
    return sb.lambda_handler()(event,context)

def findNumber(university):
    # Taking input from user through alexa and add it to this
    userInput = ""
    searchString = userInput+"+Counseling+and+Psychological+Services"

    #Format the String if needed
    searchString = searchString.replace(' ', '+') 

    #Open Chrome
    browser = webdriver.Chrome() 

    #Go to the google search results
    matched_elements = browser.get("https://www.google.com/search?q=" +searchString) 
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
    
    return proofedPhones

