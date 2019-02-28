# scrink

======FILES======

======input.csv======
Contains input email ids to be searched on thumbtube.

======output.csv======
contains the scraped data which includes first name, last name,linkedin url designation, company, location.


======script.py=======
Python script for scraping data.
======>>Functions
	1. broweser_init()= initiates a headless firefox window.
	2. site_login()= logs in to test account.
	3. profile_search()= searches for profile on thumbtube.
	4. get_deatils()= extracts data from linkedin profile. 

======NOTE======
Currently the extraction is limited to 50 accounts daily because of lack of API access by Linkedin, contact me if you know how to bypass this limit! :)
