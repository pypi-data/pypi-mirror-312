#with python we automate it
#pip isntall selenium
#by selenium we can automate any website, it also automate in physical from 

from selenium import webdriver
from selenium.webdriver.common.by import By #to get id 
from selenium.webdriver.support.ui import WebDriverWait #load and wait till it's done laod and wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
#pip install webdriver
from webdriver_manager.chrome import ChromeDriverManager #by this no manually download its will automatically do if
from os import getcwd #to find the file  the file we want to automate.By this if we share on the on any other computer it can also run there 

chrome_options= webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream") #this works whenever we visit our o/p page its asks for mike permission it will bipass it
chrome_options.add_argument("--headless=new") #its opens in background

driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
website="https://allorizenproject1.netlify.app/"

driver.get(website)

rec_file=f"{getcwd()}\\input.txt"   

def listen():
    try:
        start_button=WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.ID,'startButton')))
        start_button.click()
        print("Listening..")
        output_text=""
        
        while True:
            output_element=WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID,'output')))
            current_text=output_element.text.strip()
                       #Start Listning
            if current_text and current_text !=output_text:
                   output_text=current_text
                   with open(rec_file,"w") as file:
                    file.write(output_text.lower())
                    print("USER: "+ output_text)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
        

listen()   