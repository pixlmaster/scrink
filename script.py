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


thumbtube_link="https://www.linkedin.com/sales/gmail/profile/viewByEmail/"
user_name="testkgp@gmail.com"
user_password="qwerasdf"
linkedin_link="https://www.linkedin.com/"

def browser_init():
	_browser_profile = webdriver.FirefoxProfile()
	_browser_profile.set_preference("dom.webnotifications.enabled", False)
	options = Options()
	options.add_argument("--headless")

	driver=webdriver.Firefox(firefox_profile=_browser_profile)
	#driver=webdriver.Firefox(firefox_profile=_browser_profile,options=options)

	return driver

def site_login(browser):
	browser.get(linkedin_link)
	WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.ID,"login-email")))
	
	user=browser.find_element_by_id("login-email")
	user.send_keys(user_name)
	
	password=browser.find_element_by_id("login-password")
	password.send_keys(user_password)
	
	login_button=browser.find_element_by_id("login-submit")
	login_button.click()

def profile_search(browser,email):
	browser.get(thumbtube_link+email)
	profile_soup=bs(browser.page_source, 'html.parser')
	profile_link_find=profile_soup.find('a')
	profile_link=profile_link_find['href']
	if(profile_link!="https://www.linkedin.com/help/sales-navigator"):
		return profile_link
	else:
		return "none"

def get_details(browser,profile_link):
	browser.get(profile_link)
	soup=bs(browser.page_source,'html.parser')


driver=browser_init()
site_login(driver)

with open('input.csv') as input:
	read=csv.reader(input, delimiter=',')
	for row in read:	
		email_id=row[0];
		if(email_id!="Email_Id"):
			linkedin_profile_link = profile_search(driver,email_id)
			get_details(driver,linkedin_profile_link)