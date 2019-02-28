import os
from bs4 import BeautifulSoup as bs                              

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.firefox.options import Options

import requests
import csv

#constants
thumbtube_link="https://www.linkedin.com/sales/gmail/profile/viewByEmail/"
user_name="testkgp100@gmail.com"													#test-email id
user_password="qwerasdf"														#test-password
linkedin_link="https://www.linkedin.com/"

def browser_init():
	#initates headless firefox browser with required options
	_browser_profile = webdriver.FirefoxProfile()
	_browser_profile.set_preference("dom.webnotifications.enabled", False)
	
	options = Options()
	options.add_argument("--headless")

	driver=webdriver.Firefox(firefox_profile=_browser_profile,options=options)

	return driver

def site_login(browser):
	#Log in to liinked in
	browser.get(linkedin_link)
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID,"login-email")))
	
	user=browser.find_element_by_id("login-email")
	user.send_keys(user_name)
	
	password=browser.find_element_by_id("login-password")
	password.send_keys(user_password)
	
	login_button=browser.find_element_by_id("login-submit")
	login_button.click()

def profile_search(browser,email):
	#Search for Profile usin thumbrule
	browser.get(thumbtube_link+email)
	#make soup of current page
	profile_soup=bs(browser.page_source, 'html.parser')
	#find profile link
	profile_link_find=profile_soup.find('a')
	profile_link=profile_link_find['href']
	
	if(profile_link!="https://www.linkedin.com/help/sales-navigator"):
		name=browser.find_element_by_xpath("//span[@id='li-profile-name']")
		#find location
		locate=name.find_element_by_xpath("//div[@class='li-user-location']")
		#find first name and last name
		fname=name.get_attribute("data-fname")
		lname=name.get_attribute("data-lname")
		
		return profile_link,fname,lname,locate.text
	else:
		return "none","none","none","none"

def get_details(browser,profile_link):
	browser.get(profile_link)
	#finding company
	company=browser.find_element_by_xpath("//span[@id='ember61']")
	company_working=company.text
	
	try:
		#for 1st format of designation
		designation=browser.find_element_by_xpath("//div[@class='pv-entity__summary-info-v2 pv-entity__summary-info--background-section pv-entity__summary-info-margin-top ']/h3[@class='t-14 t-black t-bold']")
	except Exception as e:
		#for 2nd format of designation
		designation=browser.find_element_by_xpath("//div[@class='pv-entity__summary-info pv-entity__summary-info--background-section ']/h3[@class='t-16 t-black t-bold']")
	person_designation=designation.text
	
	return company_working,person_designation

driver=browser_init()

site_login(driver)

#open input file to read inputs
with open('input.csv') as input:
	#open new output file for writing
	with open('output.csv', 'w',newline='') as output:
		read=csv.reader(input, delimiter=',')
		
		write=csv.writer(output)
		write.writerow(['Email_ID','Profile URL','First name','Last name','Company Working','Designation','Location'])
		
		for row in read:	
			email_id=row[0];
			if(email_id!="Email_Id"):
				try:
					#get details of each email id(Currently Limited to 50 because of Linkedin Policy for free accounts)
					linkedin_profile_link,first_name,last_name,location = profile_search(driver,email_id)
					if(linkedin_profile_link!="none"):
						company,designation=get_details(driver,linkedin_profile_link)
					else:
						company="none"
						designation="none"
					write.writerow([email_id,linkedin_profile_link,first_name,last_name,company,designation,location])
					#give exception in case of error
				except Exception as e:
					print(e)