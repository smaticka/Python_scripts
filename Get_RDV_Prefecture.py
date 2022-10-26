#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 18:38:34 2022

This script is designed to check for available 
appointments at the Prefecture. If one is available, 
the appointment will be requested on the webserver 
(that is opened by this script), and an email will 
be sent to myself. Upon receiving the email, I must 
go to the webserver to complete the process. The 
laptop needs to stay open for this, unless running 
on a server. 

A password needs to be added in the parameter 'app_generated_password'. 
It was removed from this script for security. 

@author: maticka
"""
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

import smtplib
from email.message import EmailMessage

# In[]:
n_min = 7 # min, number of minutes to wait before checking again.


# In[]: define function to send email
def sendMail():
    
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    
    # app generated password from gmail site (insert between quotes)
    app_generated_password = ""  
    
    server.login("smaticka@gmail.com", app_generated_password)
    
    subject  = "RDV Available at PREFECTURE"
    bodyText = "Hi Sam,\n Go here: https://www.herault.gouv.fr/booking/create/15259/0\n see you soon,\nSam"
    
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = "smaticka@gmail.com"
    message["To"] = "smaticka@gmail.com"
    message.set_content(bodyText)
    
    server.sendmail("smaticka@gmail.com", "smaticka@gmail.com", message.as_string())
    

# In[]: Count number of attempts
print('Started at: {}'.format(datetime.now()))

status = 'Unavailable'

count = 0 # count the number of times checked

# In[]: Open URL in Chrome

# webdriver to talk to
driver = webdriver.Chrome(ChromeDriverManager().install())

# make request to the driver
driver.get('https://www.herault.gouv.fr/booking/create/15259/0')

# In[]: continue to check if appointment every 10 minutes
# keep log of time checked and count. 
while status != 'Complete':
    # get element of the box to click
    click_box = driver.find_element_by_xpath('//*[@id="condition"]')

    # click the box
    click_box.click()

    # get element for the go box
    go_button = driver.find_element_by_xpath('//*[@id="submit_Booking"]/input[1]')

    # click go
    go_button.click()

    # check if resulting page says no appointments
    body_text = driver.find_element_by_xpath('//*[@id="FormBookingCreate"]').text

    # check if the message tells me there are no more appointments
    if "Il n'existe plus de plage horaire libre pour votre demande de rendez-vous" in body_text:
        # print out how many times searched so far
        count += 1
        print(count)
        
        # end the search and try again
        terminate_button = driver.find_element_by_xpath('//*[@id="submit_Booking"]/input')
        
        # click end
        terminate_button.click()
        
        time.sleep(n_min*60) # check every n_min (number of minutes)
    else:
        # send alarm to myself
        sendMail()
        
        # Print out when the search finished, how many times it was searched, and the new results on the site when trying to book
        print('\nFinished at: {}'.format(datetime.now()))
        print('\nCheck {} times'.format(count))
        print('\nNew Status: {}'.format(body_text))
    
        status = 'Complete'
    
    
    
    
    
    
    

