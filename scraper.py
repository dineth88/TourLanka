import os.path
import re
import shutil
import time
import traceback
from typing import KeysView
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from faker import Faker
from wasabi import msg
from seleniumbase import Driver
import json

options = webdriver.ChromeOptions()
options.add_argument("start-maximized") 
options.add_argument("disable-infobars") 
options.add_argument("--disable-extensions")  
options.add_argument("--no-sandbox") 
# self.options.add_argument('--headless')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('accept-encoding=gzip, deflate, br, zstd')
options.add_argument('accept-language=en-US,en;q=0.9,es;q=0.8')
options.add_argument("--disable-blink-features=AutomationControlled")

mapping = [
            {'name':'Sigiriya', 'target_prompt':'Historical explanation'},
            {'name':'Yala', 'target_prompt':'Importance and uniqueness'},
            {'name':'Hurulu Eco Park', 'target_prompt':'Importance and uniqueness'},
            {'name':'Polonnaruwa Gal Viharaya, Museum & Kingdom', 'target_prompt':'Historical explanation'},
            {'name':'Udawalawa', 'target_prompt':'Importance and uniqueness'},
            {'name':'Mirissa', 'target_prompt':'Importance and uniqueness'},
            {'name':'Jethawanaya', 'target_prompt':'Historical explanation'},
            {'name':'Horton Plains', 'target_prompt':'Importance and uniqueness'},
            {'name':'Wilpattu', 'target_prompt':'Importance and uniqueness'},
            {'name':'Buduruwagala', 'target_prompt':'Historical explanation'},
            {'name':'Sinharaja Conservation Forest', 'target_prompt':'Importance and uniqueness'},
            {'name':'Badulla Haputhale', 'target_prompt':'Importance and uniqueness'},
            {'name':'Galle', 'target_prompt':'Importance and uniqueness'},
            {'name':'Jaffna Fort', 'target_prompt':'Historical explanation'},
            {'name':'Minneriya', 'target_prompt':'Historical explanation'},
            {'name':'Ritigala Forest', 'target_prompt':'Historical explanation'},
            {'name':'Udawattakele Conservation Forest', 'target_prompt':'Importance and uniqueness'},
            {'name':'Bundala', 'target_prompt':'Importance and uniqueness'},
            {'name':'Kumana', 'target_prompt':'Importance and uniqueness'},
            {'name':'Galoya', 'target_prompt':'Historical explanation'},
            {'name':'Pigeon Island', 'target_prompt':'Importance and uniqueness'},
        ]

url='https://www.perplexity.ai/'
count = 0
context = ''
print('========================= Historical Data ========================')

driver = Driver(uc=True, headless=False)
driver.maximize_window()
try:
    for i in range (0, 6):
        try:
            driver.get(url)
            time.sleep(20)
            prompt_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Ask anything..."]')
            break
        except:
            print("Issue")
            pass
except:
    traceback.print_exc()

wait = WebDriverWait(driver, 40)

for map_item in mapping:
    print(f'========================= {map_item["name"]} ========================')

    #prompt submission
    try:
        time.sleep(30)
        if(count==0):
            prompt_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Ask anything..."]')
        else:
            prompt_input = driver.find_element(By.XPATH, '//textarea[@placeholder="Ask follow-up"]')
        prompt_input.send_keys(f"I need information about some Sri Lankan travel location to put into my blog website. Provide me nearly 1000 words about {map_item['target_prompt']} of {map_item['name']}. State the whole contents in json format as 'location':'{map_item['name']}',historical data: {map_item['target_prompt']} format. Only provide the json data answer by restricting to the given format for me. Do not add any partitions or topic to divide to historical data into parts like importance, early history etc. Just state the whole answer like one paragraph inside historical data.")
        time.sleep(10)
    except:
        traceback.print_exc()
        print(traceback.format_exc())
        pass 

    try:
        if(count==0):
            popup_close = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="focus-visible:bg-offsetPlus dark:focus-visible:bg-offsetPlusDark md:hover:bg-offsetPlus text-textOff dark:text-textOffDark md:hover:text-textMain dark:md:hover:bg-offsetPlusDark  dark:md:hover:text-textMainDark font-sans focus:outline-none outline-none outline-transparent transition duration-300 ease-out font-sans  select-none items-center relative group/button  justify-center text-center items-center rounded-full cursor-pointer active:scale-[0.97] active:duration-150 active:ease-outExpo origin-center whitespace-nowrap inline-flex text-sm h-8 aspect-square"]')))
            popup_close[2].click()
    except:
        traceback.print_exc()
        print(traceback.format_exc())
        pass

    try:
        btn_submit = wait.until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Submit"]'))).click()
        msg.good("Prompt submitted successfully")
        time.sleep(10) 
    except:
        traceback.print_exc()
        print(traceback.format_exc())
        pass  
     
    count+=1 

# Capturing info
try:
    time.sleep(15)
    # answer_context = driver.find_elements(By.XPATH, '//p[@class="my-0"]')
    answer_context = driver.find_elements(By.XPATH, '//span[contains(@class, "token")]')

    # Extract text and join
    context = "".join([answer.text.replace('\\', '') for answer in answer_context])

    msg.good("Answer captured successfully")
except Exception as e:
    print(e)
    print(traceback.format_exc())

formatted_data = "[" + context.replace("}{", "},{") + "]"  # Fix JSON by adding commas between objects

msg.good(f"{formatted_data}")
# Parse JSON string into Python objects
parsed_data = json.loads(formatted_data)

# Convert to required format
formatted_result = [
    {"location": item["location"], "historicalData": item["historical data"]}
    for item in parsed_data
]



# Save to JSON file
json_file = "location_data.json"
with open(json_file, "w", encoding="utf-8") as file:
    json.dump(formatted_result, file, indent=2, ensure_ascii=False)

print(f"JSON file saved as {json_file}")
