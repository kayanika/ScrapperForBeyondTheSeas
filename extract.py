import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service


# Set up the Chrome web driver
#pythoos.environ['PATH'] += "/usr/bin/chromedriver"
service = Service()
chrome_options=Options()
chrome_options.add_experimental_option("detach", True)
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'


chrome_options.add_argument('--disable-gpu')


#chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent={user_agent}')

chrome_options.add_argument("--window-size=600,600")
# options.page_load_strategy = 'none'

#driver = webdriver.Chrome(options=chrome_options)
driver=uc.Chrome(headless=False,use_subprocess=False,service=service)


# Open the MIT University website
url = 'https://www.phdportal.com/'
driver.get(url)
driver.get_screenshot_as_file("screenshot.png")
time.sleep(10)
driver.implicitly_wait(10)
element=driver.find_element(By.ID, "DisciplineSpotlight")
print(element.text)
clickableElements=driver.find_elements(By.CSS_SELECTOR, 'li[data-clickable="clickable"]')
print(len(clickableElements))
print(len(clickableElements))
for Celement in clickableElements:
    driver.implicitly_wait(20)
    time.sleep(10)
    el=Celement.find_element(By.CSS_SELECTOR, 'a')
    print(el.text)
    #ActionChains(driver).move_to_element(el).send_keys(Keys.ENTER).perform()
    driver.execute_script("return arguments[0].click();", el); 

    #print clicked
    driver.get_screenshot_as_file("screenshot.png")
    print("clicked")
    time.sleep(5)
    elementInside=driver.find_element(By.CLASS_NAME, "DisciplineConversion")
    link=elementInside.find_element(By.CSS_SELECTOR, 'a')
    print(link.text)
    #time.sleep(10)
    driver.execute_script("return arguments[0].click();", link); 
    time.sleep(5)
    #now inside all programs
    driver.get_screenshot_as_file("screenshot1.png")
    
    for i in range(1, 4):
        result=driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div/main/div/div/div/div/article/section/ul/li[{i}]/a')
        #link=result.find_element(By.CSS_SELECTOR, 'a')
        time.sleep(5)
        #link=result.get_attribute('href')
        
        driver.execute_script("return arguments[0].click();", result); 
        #switc to new window
        #driver.get(link)
        print("clicked")
        time.sleep(3)
        print(driver.current_url)
        #WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))
        print(driver.window_handles)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(10)
        driver.get_screenshot_as_file("screenshot3.png")
        #close this window
        driver.close()

        #switch back to main window
        driver.switch_to.window(driver.window_handles[0])
        driver.back()
    
   
        

    
    driver.back()
    time.sleep(10)
    driver.back()
    time.sleep(10)
   # driver.get_screenshot_as_file("screenshot1.png")

# # Find the relevant elements containing program names and tuition fees
# program_elements = driver.find_elements_by_css_selector('.program-name')   # Replace with actual CSS selector
# tuition_fee_elements = driver.find_elements_by_css_selector('.tuition-fee')  # Replace with actual CSS selector

# # Extract data from the elements
# programs = [program.text for program in program_elements]
# tuition_fees = [fee.text for fee in tuition_fee_elements]

# # Print the extracted data
# for program, fee in zip(programs, tuition_fees):
#     print(f"Program: {program} | Tuition Fee: {fee}")

# # Close the web driver
#driver.quit()
