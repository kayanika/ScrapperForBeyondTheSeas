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
from db import db_connection
conn=db_connection()
cur=conn.cursor()


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
time.sleep(4)
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
    #cur.execute("INSERT INTO fieldofinterest (field) VALUES (%s)", (el.text,))
    #check if field already exists
    cur.execute("SELECT * FROM fieldofinterest WHERE field=%s", (el.text,))
    result=cur.fetchone()
    if result is None:
        cur.execute("INSERT INTO fieldofinterest (field) VALUES (%s)", (el.text,))
        conn.commit()
        print("inserted")
    else :
        print("already exists")    
    #this here is the name of field of interest
    

    print(result)
    
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
    
    for i in range(1, 2):
        programName=driver.find_element(By.XPATH,"/html/body/div[2]/div[1]/div/div/div[2]/section/div/header/h1/a[1]" )
        programName=programName.text
        courseName=programName
        print(programName)
       
        result=driver.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div/main/div/div/div/div/article/section/ul/li[{i}]/a')
        print(result.text)
        
        time.sleep(5)
        #I am just clicking on the program
        driver.get(result.get_attribute('href'))
        #driver.execute_script("return arguments[0].click();", result); 

        #switc to new window
        #driver.get(link)
        print("clicked")
        time.sleep(3)
        print(driver.current_url)
        
        time.sleep(5)
        #driver.get_screenshot_as_file("screenshot"+{i}+ ".png")
        #close this window
        #driver.close()
        #duration=driver.find_element(By.CLASS_NAME, "js-duration")
        duration=driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/section[1]/div/div[1]/div/div[2]/div[1]")
        duration=duration.text
        print("duration: "+duration)
        tuition=driver.find_element(By.CLASS_NAME, "TuitionFeeContainer")
        tuition=tuition.text
        print("tuition: "+tuition)
        timingElements=driver.find_elements(By.CLASS_NAME, "TimingContainer")
        for timingElement in timingElements:
            timing=timingElement.text
            print("timing: "+timing)
        name=driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/article/header/div/a[1]")
        # <a class="Name TextLink Connector js-organisation-info-link" href="/universities/11911/curtin-university.html"> Curtin University </a>
        name=name.text
        print("name: "+name)
        location=driver.find_element(By.CLASS_NAME, "LocationItems")
        location=location.text
        print("location: "+location)
        rank=driver.find_element(By.CLASS_NAME, "Ranking")
        rank=rank.find_element(By.CLASS_NAME, "Value")
        rank=rank.text
        print("rank: "+rank)
        rating=driver.find_element(By.CLASS_NAME, "Rating")
        rating=rating.find_element(By.CLASS_NAME, "Value")
        rating=rating.text
        print("rating: "+rating)
        #insert into program table - programName, duration, scholashipAvailable, tuituinfee,availablescholarship number
        query="INSERT INTO program (program_type, duration, scholarship_available,tuition_fees, available_scholarships) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (programName, duration,'TRUE', int(tuition),1))
        conn.commit()
        print("inserted into program table")
        #insert inti course table - courseName, tuitonfee
        query="INSERT INTO course (course_name, tuition_fees) VALUES (%s, %s)"
        cur.execute(query, (courseName, int(tuition))) #ANIKA : CHECK IF THIS WORKS
        conn.commit()
        print("inserted into course table")
        # get the program ID and course ID
        cur.execute("SELECT program_id FROM program WHERE program_type=%s", (programName))
        programID=cur.fetchone()
        cur.execute("SELECT course_id FROM course WHERE course_name=%s", (courseName))
        courseID=cur.fetchone() 
        

        #insert into programmecoursemapping table - program ID, course ID
        query="INSERT INTO programmecoursemapping (program_id, course_id) VALUES (%s, %s)" 
        cur.execute(query, (programID, courseID))
        conn.commit()     
        
        #check if this university already insert into university table, then insert the university
        cur.execute("SELECT * FROM university WHERE university_name=%s", (name))
        result=cur.fetchone()
        if result is None:
            query="INSERT INTO university (university_name, location, ranking, rating) VALUES (%s, %s, %s, %s)"
            cur.execute(query, (name, location, rank, rating))
            conn.commit()
        #insert into universityrunsprogram table - university ID, program ID
        cur.execute("SELECT university_id FROM university WHERE university_name=%s", (name,))
        universityID=cur.fetchone()
        query="INSERT INTO universityrunsprogram (university_id, program_id) VALUES (%s, %s)"
        cur.execute(query, (universityID, programID))
        conn.commit()
        #switch back to main window
        #driver.switch_to.window(driver.window_handles[0])
        driver.back()
        print(driver.current_url)
        #driver.get_screenshot_as_file("screenshot4.png")
    
   
        

    
    driver.back()
    time.sleep(5)
    driver.back()
    

driver.back()    

