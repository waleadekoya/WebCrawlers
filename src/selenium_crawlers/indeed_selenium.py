import math
import os
import pathlib
import sys
import time

import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

print("added to sys path: ", pathlib.Path(__file__).parent.parent.__str__())
sys.path.append(pathlib.Path(__file__).parent.parent.__str__())

from utils.selenium_webdriver import driver
from utils.stmp_server import SendMultipartEmail
from utils.config import indeed_search_word
# # selenium 4
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
#
# from utils.stmp_server import SendMultipartEmail
#
# # options to add as arguments
#
# user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
# option = webdriver.ChromeOptions()
# option.add_argument("start-maximized")
# option.add_argument("--headless")
# option.add_argument("--window-size=1920,1080")
# option.add_argument(f'user-agent={user_agent}')
#
base_url = f'https://uk.indeed.com/jobs?q={indeed_search_word}&fromage=7'
#
# # chrome to stay open
# option.add_experimental_option("detach", True)
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

driver.get(base_url)
time.sleep(2)
URL = []
# https://selenium-python.readthedocs.io/locating-elements.html

page_text = driver.find_element(By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount").text

print(page_text)
if "Page 1 of " in page_text:
    results_count = int(page_text.replace("Page 1 of ", '').replace(" jobs", ''))
else:
    results_count = int(page_text.replace(" jobs", ''))
print("Total number of jobs:", results_count)
page_count = math.ceil(results_count / 15)
print("Total number of pages:", page_count)


def get_salary(url: str):
    driver.get(url)
    try:
        return {"salary": driver.find_element(By.CSS_SELECTOR, 'span.icl-u-xs-mr--xs').text}
    except NoSuchElementException as e:
        return {"salary": None}


results = [{
    'title': url.text,
    'url': driver.find_element(By.LINK_TEXT, url.text).get_attribute('href'),
}
    for url in driver.find_elements(By.XPATH, '//h2[@class="jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0"]')
]
results = [{**value, **get_salary(value['url'])} for value in results]

if page_count > 1:
    for page in range(1, page_count):
        print(f"crawling page {page + 1} of {page_count}...")
        next_page_url = base_url + f"&start={page * 10}"
        print(next_page_url)
        driver.get(next_page_url)
        data = [{
            'title': url.text,
            'url': driver.find_element(By.LINK_TEXT, url.text).get_attribute('href'),
        }
            for url in driver.find_elements(By.XPATH, '//h2[@class="jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0"]')
        ]
        data = [{**value, **get_salary(value['url'])} for value in data]
        print(data)
        results.extend(data)

df = pd.DataFrame(results).drop_duplicates().reset_index(drop=True)
driver.quit()
print(df)

SendMultipartEmail(
    subject='KYC Analyst Indeed Jobs',
    sender='wale.adekoya@btinternet.com',
    recipients='chezyfive@yahoo.com,favour.adekoya@yahoo.com,wale.adekoya@btinternet.com',
    attachment_body=df.to_html(index=False, col_space='100px')
)
