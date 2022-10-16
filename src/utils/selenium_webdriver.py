import math
import os
import time

import pandas as pd
# selenium 4
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from utils.stmp_server import SendMultipartEmail

# options to add as arguments

user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
option = webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_argument("--headless")
option.add_argument("--window-size=1920,1080")
option.add_argument(f'user-agent={user_agent}')

base_url = 'https://uk.indeed.com/jobs?q=kyc+aml&fromage=7'

# chrome to stay open
option.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

driver.get(base_url)
time.sleep(2)