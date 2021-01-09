from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass
import os.path
PATH = "C:\Program Files (x86)\chromedriver.exe"

# Our canvas website has an issue of having two entries for the same date
# Because their CSS selector names are not unique and their class id is not unique we cannot grab just one
# and end up grabbing a short hand and a long hand of the same date i.e. Jan 3 vs January 3rd
# We will split the elements by new line (They are on separate lines) and take the longer string i.e. January 3rd
# Store this to a List and return
def parseDates(dates):
    result =  []
    for date in dates:
        tempDate = date.split('\n');
        result.append(max(tempDate, key=len))
    return result
# If we have run the program before, we will use the previously provided Canvas link
# This assumes we only attend one University at a time
try:
    urlFile = open('CanvasLoginLink.txt', 'r')
    canvasLink = urlFile.read()
    urlFile.close()
# If we haven't run the program before we will store the Canvas link to a text file
# Next time we run the program, we will use the text file instead of prompting the user for the link again
except FileNotFoundError:
    canvasLink = input('Please enter your login page url (Include http://): ')
    urlFile = open('CanvasLoginLink.txt', 'w')
    urlFile.write(canvasLink)
    urlFile.close()
# Input username and password (Note: password will not show the input keys for privacy)
userName = input('Username: ')
passWord = getpass.getpass('Password: ')
# Use the Canvas link to get to the website
driver = webdriver.Chrome(PATH)
driver.get(canvasLink)
# Wait to make sure everything loads
# Then input the username and password provided in the fields and press the login button
driver.implicitly_wait(5)
userLogin = driver.find_element_by_name('j_username')
userLogin.send_keys(userName)
userPass = driver.find_element_by_name('j_password')
userPass.send_keys(passWord)
loginButton = driver.find_element_by_name('_eventId_proceed')
loginButton.click()
# Navigate to the calendar webpage in Canvas
driver.get(canvasLink + "/calendar")
# Wait for the webpage to load then go to the Agenda tab by clicking the button
driver.implicitly_wait(5)
agendaButton = driver.find_element_by_xpath('//*[@id="agenda"]')
agendaButton.click()
# Find the title which would be the current date, we will use this for our output file
title = driver.find_element_by_class_name('navigation_title')
summaryFile = open("Month of " + title.text + " Agenda.txt", "w")
# Allow contents of Agenda to load
driver.implicitly_wait(15)
# Parse through the data and store to lists as WebElements
agendaDates = driver.find_elements_by_class_name('agenda-day')

allAgenda = driver.find_elements_by_class_name('agenda-event__list')
# Convert the WebElements in the dates List to strings
# We have to do this because we need to account for the duplicate dates hence our first function
# Jan 3 vs January 3rd
temp = []
for date in agendaDates:
    temp.append(date.text)
dates =  parseDates(temp)
# Now just iterate through each date
# For each date we will process the respective agenda elements and output to the file
for i in range(len(dates)):
    summaryFile.write(dates[i] + '\n')
    allEvents = allAgenda[i].find_elements_by_class_name('agenda-event__title')
    allTimes = allAgenda[i].find_elements_by_class_name('agenda-event__time')
    for i in range(len(allEvents)):
        summaryFile.write(allTimes[i].text + ' ' + allEvents[i].text + '\n')
    # Add extra line between dates for clarity
    summaryFile.write('\n')
# Close file and driver
summaryFile.close()
driver.quit()
