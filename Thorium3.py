# TODO:
# 1) VALIDATED, If password file is empty pause on login page and prompt to enter password
# 2) VALIDATED, Fix trailing whitespaces and single line job_name after rip 
# 3) VALIDATED, Make autosys standard delimiter format 
# 4) VALIDATED, Auto commit is broken 

# # Import packages needed for GUI
from tkinter import *

# Import needed packages for engine 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys 
import os

# Define function to kill the application in the event of an issue and return an error to the user 
##################################################################################################
def kill(msg):
    # Print error then kill program 
    def Exit():
        sys.exit()

    root = Tk()

    label_open1 = Label(root, text = msg).pack()
    button1 = Button(root, text='Exit', command=Exit).pack()
##################################################################################################

# Try to get username and password 
###########################################################################################################
username = ''
with open('C:/Thorium/Credentials/user.txt', 'r') as usr:
    for line in usr:
        username = line.strip()

if username == '':
    #kill("No username specified in C:\Thorium\Credentials\user.txt")
    pass

password = ''
with open('C:/Thorium/Credentials/pass.txt', 'r') as passw:
    for line in passw:
        password = line.strip()
###########################################################################################################

# Launch GUI and ask if the user wants to download or upload a JIL 
def download():
    global choice 
    choice = 'down'

    root.destroy() 

def upload():
    global choice 
    choice = 'up'

    root.destroy() 

root = Tk()

label_open1 = Label(root, text = 'Welcome to Thorium - Autosys Dev version').pack()

# # Display Thorium image
# img = ImageTk.PhotoImage(Image.open("C:\Thorium\Support\Images\Thorium.jpg"))
# panel = Label(root, image = img)
# panel.pack(side = "bottom", fill = "both", expand = "no")

label_open2 = Label(root, text = 'Do you want to Upload a JIL or Download a JIL').pack()

button1 = Button(root, text='Upload', command=upload).pack()
button2 = Button(root, text='Download', command=download).pack()

root.mainloop()

# End of GUI section 

# If choice was upload, then run upload section 
if choice == 'up':

    # Launch GUI and allow user to specify values for required variables. 
    # Define variables and then end the program 
    def get_variable_value():
        global path, review
        path = str_path.get()
        review = str_review.get()

        root.destroy() 

    root = Tk()

    str_path = StringVar()
    str_review = StringVar()
    valueresult = StringVar()

    label_open = Label(root, text = 'Welcome to Thorium - Autosys Dev version').pack()

    labelp = Label(root, text = 'Please provide full name and path combination of JIL file').pack()
    path_ = Entry(root, justify='left', width=100, textvariable = str_path).pack() 

    labelr = Label(root, text = 'Specify "Y" if you would like to review the uploads before committing').pack()
    review_ = Entry(root, justify='left', width=2, textvariable = str_review).pack() 

    button = Button(root, text='Go', command=get_variable_value).pack()

    root.mainloop()

    # End of GUI section 

    # JIL class that will create a JIL object from a JIL string 
    class JIL(object):

        '''
        Args: 
            jil: JIL file as a string.
        
        Returns:
            JIL object with JIL fields as object attributes.

        '''

        def __init__(self, jil):
            self.jil = jil

            for line in self.jil.splitlines():
                setattr(self, line.partition(": ")[0], line.partition(": ")[2])

    # Define the main function 
    def upload_main():

        '''
        Args: 
            Receives command line args if provided.
        
        Returns:
            Runs Selenium code and populates Autosys website with JIL input.

        Raises:
            AssertionError: "No JIL file found" if no JIL input is provided.

        '''

        if path != '':
            # Create the instance of the object, check if JIL file was specified in script 
            filename = path
            file2 = ''
            line_count = 0
            with open(filename, 'r') as file:
                for line in file:
                    if line_count == 0:
                        line = 'DELETE'
                    if line == '':
                        line = 'DELETE'
                    if '/* -----------------' in line:
                        line = '/*\n'
                    line = line.strip()
                    line = line+'\n'
                    if line != '\n' and 'DELETE' not in line:
                        file2 += line
                    line_count += 1
            jil_jobs = file2.split('/*')
        else:
            raise AssertionError("No JIL file found")

        # Init driver
        driver = webdriver.Chrome(executable_path='C:/Thorium/Support/chromedriver.exe')

        driver.get("<SUPPLY AUTOSYS DEV PATH>")

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

            sleep(4)
        else:
            # Wait for the user to enter password manually and log in 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT, 'Quick Edit')))

        ######### Start loop for each JIL job ###########
        for job in jil_jobs:
            jil = JIL(job)

            sleep(2)

            driver.switch_to.default_content()

            # Wait for next element to load 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.LINK_TEXT, 'Quick Edit')))

            # Click Quick Edit 
            driver.find_element_by_link_text("Quick Edit").click()

            sleep(2)

            # Click createObject
            driver.switch_to_frame(driver.find_element_by_id("QuickEdit"))  ##switch it

            # Wait for next element to load 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.NAME, 'createObject')))

            driver.find_element_by_name("createObject").click()

            # Wait for next element to load 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.NAME, '_blank')))

            # Switch to _blank frame 
            driver.switch_to_frame(driver.find_element_by_name("_blank"))  ##switch it

            # Wait for next element to load 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="objectTypes"]/table[2]/tbody/tr[5]/td/div/table/tbody/tr/td[3]/a')))

            # If Box then choose box type 
            if "BOX" in jil.job_type.upper():

                # Click Box 
                driver.find_element_by_xpath('//*[@id="objectTypes"]/table[2]/tbody/tr[3]/td/div/table/tbody/tr/td[3]/a').click()

                sleep(3)

                # Switch back to QuickEdit frame
                driver.switch_to_frame(driver.find_element_by_id("QuickEdit"))  ##switch it

                # Start populating JIL template in GUI 
                # insert_job
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:1:InputText"]')
                    write.send_keys(jil.insert_job)
                except:
                    pass
                
                # condition
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:3:InputTextMultiple"]')
                    write.send_keys(jil.condition)
                except:
                    pass

                # owner
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:5:InputText"]')
                    write.send_keys(jil.owner)
                except:
                    pass

                # box_name
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:6:SearchInput"]')
                    write.send_keys(jil.box_name)
                except:
                    pass

                # max_run_alarm
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:35:InputText"]')
                    write.send_keys(jil.max_run_alarm)
                except:
                    pass

                # send_notification
                try:
                    if jil.send_notification == "n":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:37:CheckBox"]')
                        write.click()
                except:
                    pass

                # permission == gx
                try:
                    if jil.permission == "gx":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:51:CheckBox"]')
                        write.click()
                except:
                    pass

            # If CMD then choose box type 
            if "CMD" in jil.job_type.upper():
                # Click Box 
                driver.find_element_by_xpath('//*[@id="objectTypes"]/table[2]/tbody/tr[4]/td/div/table/tbody/tr/td[3]/a').click()

                sleep(3)

                # Switch back to QuickEdit frame
                driver.switch_to_frame(driver.find_element_by_id("QuickEdit"))  ##switch it

                # Start populating JIL template in GUI 
                # insert_job
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:1:InputText"]')
                    write.send_keys(jil.insert_job)
                except:
                    pass
                
                # machine 
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:3:SearchInput"]')
                    write.clear()
                    write.send_keys(jil.machine)
                except:
                    pass

                # condition
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:4:InputTextMultiple"]')
                    write.send_keys(jil.condition)
                except:
                    pass

                # owner
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:6:InputText"]')
                    write.send_keys(jil.owner)
                except:
                    pass

                # command
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:12:InputTextMultiple"]')
                    write.send_keys(jil.command)
                except:
                    pass

                # box_name
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:7:SearchInput"]')
                    write.send_keys(jil.box_name)
                except:
                    pass

                # std_err_file
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:19:InputText"]')
                    write.send_keys(jil.std_err_file)
                except:
                    pass

                # max_run_alarm
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:54:InputText"]')
                    write.send_keys(jil.max_run_alarm)
                except:
                    pass

                # send_notification
                try:
                    if jil.send_notification == "n":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:55:CheckBox"]')
                        write.click()
                except:
                    pass

                # permission == gx
                try:
                    if jil.permission == "gx":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:69:CheckBox"]')
                        write.click()
                except:
                    pass

            # If FW then choose box type 
            if "FW" in jil.job_type.upper():
                # Click Box 
                driver.find_element_by_xpath('//*[@id="objectTypes"]/table[2]/tbody/tr[5]/td/div/table/tbody/tr/td[3]/a').click()

                sleep(3)

                # Switch back to QuickEdit frame
                driver.switch_to_frame(driver.find_element_by_id("QuickEdit"))  ##switch it

                # Start populating JIL template in GUI 
                # insert_job
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:1:InputText"]')
                    write.send_keys(jil.insert_job)
                except:
                    pass
                
                # machine 
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:3:SearchInput"]')
                    write.clear()
                    write.send_keys(jil.machine)
                except:
                    pass

                # condition
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:4:InputTextMultiple"]')
                    write.send_keys(jil.condition)
                except:
                    pass

                # owner
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:6:InputText"]')
                    write.send_keys(jil.owner)
                except:
                    pass

                # box_name
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:7:SearchInput"]')
                    write.send_keys(jil.box_name)
                except:
                    pass

                # watch_file
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:12:InputText"]')
                    write.send_keys(jil.watch_file)
                except:
                    pass

                # watch_interval
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:14:InputText"]')
                    write.send_keys(jil.watch_interval)
                except:
                    pass

                # max_run_alarm
                try:
                    write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:42:InputText"]')
                    write.send_keys(jil.max_run_alarm)
                except:
                    pass

                # send_notification
                try:
                    if jil.send_notification == "n":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:43:CheckBox"]')
                        write.click()
                except:
                    pass

                # permission == gx
                try:
                    if jil.permission == "gx":
                        write = driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:propertiesTreeTable:57:CheckBox"]')
                        write.click()
                except:
                    pass

            if review.upper() == "Y":

                # Launch GUI
                def go():

                    root.destroy() 

                root = Tk()

                labeli = Label(root, text = 'Review the content and then commit the job, when finished click "Next One" to upload the next job\n').pack()
                button = Button(root, text='Next One', command=go).pack()

                root.mainloop()
            
            else:
                sleep(1)

                # Commit the job 
                driver.find_element_by_xpath('//*[@id="propertiesSubview:propertiesForm:commit"]').click()

                sleep(3)
        
        # Launch GUI
        def go():

            root.destroy() 

        root = Tk()

        labeli = Label(root, text = 'All Done!\n').pack()
        button = Button(root, text='Exit', command=go).pack()

        root.mainloop()
        
    # Run upload main function 
    upload_main()

# If choice was download, then run download section 
if choice == 'down':

    def download_main():

        # Launch GUI and allow user to specify values for required variables. 
        # Define variables and then end the program 
        def get_variable_value():
            global jil_name
            jil_name = str_jil.get()
            jil_name.strip()

            root.destroy() 

        root = Tk()

        str_jil = StringVar()

        label_open = Label(root, text = 'Welcome to Thorium - Autosys Dev version').pack()

        labelp = Label(root, text = "Please provide the name of the box job you'd like to use to make the JIL").pack()
        jil_name_ = Entry(root, justify='left', width=100, textvariable = str_jil).pack() 

        button = Button(root, text='Go', command=get_variable_value).pack()

        root.mainloop()

        # End of GUI section 

        # Init driver
        driver = webdriver.Chrome(executable_path='C:/Thorium/Support/chromedriver.exe')

        driver.get("<SUPPLY AUTOSYS DEV PATH>")

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

        # Wait for next element to load 
        element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="boxJobResultTable:0:hgi"]/img')))
        
        # Get BOX JIL
        # Init the string that JIL will be written to
        jil_consol = ""
        
        driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()
        # Wait for next element to load 
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
        for elem in elems:
            if jil_name[:8] in str(elem.get_attribute("href")) and jil_name.strip() not in str(elem.get_attribute("href")):
                selects.append(str(elem.get_attribute("href")))

        # Get the rest of the Jobs
        # Loop through and capture each JIL 
        for item in selects:

            driver.get(item)

            # Wait for next element to load 
            element = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jilButtonID"]')))

            driver.find_element_by_xpath('//*[@id="jilButtonID"]').click()
            # Wait for next element to load 
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

        # Launch GUI
        def go():

            root.destroy() 

        root = Tk()

        labeli = Label(root, text = 'Success! All Done!\nYou can find your JIL file at C:\Thorium\{}.jil'.format(jil_name)).pack()
        button = Button(root, text='Exit', command=go).pack()

        root.mainloop()

    # Run upload main function 
    download_main()

