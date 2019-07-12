# Import needed packages for engine 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import sys 
import os

# Try to get username and password 
###########################################################################################################
username = ''
with open('C:/Thorium/Credentials/user.txt', 'r') as usr:
    for line in usr:
        username = line.strip()

password = ''
with open('C:/Thorium/Credentials/pass.txt', 'r') as passw:
    for line in passw:
        password = line.strip()

# Set environment to prod
###########################################################################################################
environment = 'prod'
###########################################################################################################

# Open file and create string out of it. 
boxlist = ""
listfile = open("C:\Users\ip4057\Documents\GitHub\ProdAutoSysRip\BoxListDebug.txt", "r")
for line in listfile:
    boxlist += line.strip()

finallist = boxlist.split(",")


# Init driver
driver = webdriver.Chrome(executable_path='C:/Thorium/Support/chromedriver.exe')

# Connect to the specified version of Autosys
if environment == 'dev':
    driver.get("<DEV AUTOSYS>")
elif environment == 'prod':
    driver.get("<PROD AUTOSYS>")

# Wait for next element to load 
element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="x-auto-10-input"]')))

# Authenticate page with credentials 
# write user name
write = driver.find_element_by_xpath('//*[@id="x-auto-10-input"]')
write.send_keys(username)

if password != '':
    # write password
    write = driver.find_element_by_xpath('//*[@id="x-auto-11-input"]')
    write.send_keys(password)

    sleep(2)

    # Click log in 
    login = driver.find_element_by_xpath('//*[@id="x-auto-8"]/tbody/tr[2]/td[2]/em/button')
    login.click()

    sleep(2)
else:
    # Wait for the user to enter password manually and log in 
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT, 'Quick View')))

sleep(4)

# loop through each job name
for jil_name in finallist:

    print(jil_name)

    if environment == 'prod':
        driver.get("<PROD AUTOSYS>")

    driver.switch_to.default_content()

    # Wait for next element to load 
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT, 'Quick View')))

    # Click Quick Edit 
    driver.find_element_by_link_text("Quick View").click()

    sleep(2)

    # Wait for next element to load 
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'QuickView')))

    # Switch back to QuickEdit frame
    driver.switch_to_frame(driver.find_element_by_id("QuickView"))  ##switch it

    # Wait for next element to load 
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jobNameInput"]')))

    write = driver.find_element_by_xpath('//*[@id="jobNameInput"]')
    write.send_keys(jil_name)

    driver.find_element_by_xpath('//*[@id="goButtonID"]').click()

    # Add try block to pass box jobs that only have the box and no jobs under them
    #try:
    # Wait for next element to load 
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="boxJobResultTable:0:hgi"]/img')))

    # Get BOX JIL
    # Init the string that JIL will be written to
    jil_consol = ""

    # Line below uncommented because it appars that JIL layout is automatically shown
    # driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()

    # Wait for next element to load 
    # try:
    #     driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()
    #     element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilsubPanelId"]')))
    #     sleep(1)
    # except:
    element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilsubPanelId"]')))
    sleep(1)

    get_jil=driver.find_element_by_xpath('//*[@id="jilsubPanelId"]')

    # Get job_type on the new line 
    jil_temp = str(get_jil.text)
    jil_temp = jil_temp.replace('    job_type:','\njob_type:')

    # Get job name for delimeter 
    delim_job = jil_temp.split('insert_job:')[1].split('\n')[0]
    delim_job = delim_job.rstrip()

    jil_consol += str('/* ----------------- ' + delim_job + ' ----------------- */' + '\n\n')
    jil_consol += jil_temp

    # Expand table 
    driver.find_element_by_xpath('//*[@id="boxJobResultTable:0:hgi"]/img').click()

    sleep(3)

    # Ignore dependent jobs and starting conditions sections 
    driver.find_element_by_xpath('//*[@id="nestedDetailPageSuffix:dependentAccordionId"]/div/a/img').click()
    sleep(2)
    driver.find_element_by_xpath('//*[@id="nestedDetailPageSuffix:atomicAccordionId"]/div/a').click()
    sleep(2)

    elems = driver.find_elements_by_xpath('//a[@href]')
    selects = []

    # # New section to make list of column contents
    # #table_id = driver.find_element(By.XPATH, '//*[@id="boxJobResultTable"]')
    # tbody = driver.find_element(By.XPATH, '//*[@id="boxJobResultTable"]/table[2]/tbody')
    # rows = tbody.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table
    # for row in rows:
    #     # Get the columns (all the column 2)        
    #     col = row.find_elements(By.TAG_NAME, "td") #note: index start from 0, 1 is col 2
    #     print("THIS IS COLUMN TEXT", col) #prints text from the element

    for elem in elems:
        print(elem.get_attribute("href"))
        if jil_name[:8] in str(elem.get_attribute("href")) and jil_name.strip() not in str(elem.get_attribute("href")):
            selects.append(str(elem.get_attribute("href")))

    print(selects)
    # Get the rest of the Jobs
    # Loop through and capture each JIL 
    for item in selects:

        driver.get(item)

        # Wait for next element to load 
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilButtonID"]')))
        
        # Line below uncommented because it appars that JIL layout is automatically shown
        #driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()

        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="j_id170"]/table[2]/tbody/tr[1]/th[1]')))
            driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilsubPanelId"]')))
            sleep(1)
            
        except:
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilsubPanelId"]')))
            sleep(1)
        
        get_jil=driver.find_element_by_xpath('//*[@id="jilsubPanelId"]')
        # Get job_type on the new line 
        jil_temp = str(get_jil.text)
        jil_temp = jil_temp.replace('    job_type:','\njob_type:')

        # Get job name for delimeter 
        delim_job = jil_temp.split('insert_job:')[1].split('\n')[0]
        delim_job = delim_job.rstrip()

        # Add leading space 
        jil_temp = jil_temp.replace('\n', '\n ')

        jil_consol += str('\n\n' + ' /* ----------------- ' + delim_job + ' ----------------- */' + '\n\n ')

        jil_consol += jil_temp

    # Attempt to remove any trailing whitespaces 
    jil_consol = jil_consol.rstrip()

    # Write the file out 
    output = open("C:\Thorium\{}.jil".format(jil_name),"w")
    output.write(jil_consol)
    output.close()
# except:
#     pass