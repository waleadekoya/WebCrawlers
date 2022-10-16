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
from utils.config import indeed_search_word, recipients, title

print('search word read is:', os.getenv('SEARCH_WORD'))

base_url = f"https://uk.indeed.com/jobs?q={indeed_search_word}&fromage=7"
print(f"base url:", base_url)

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
    subject=f'{title} Indeed Jobs',
    sender='wale.adekoya@btinternet.com',
    recipients=recipients,
    attachment_body=df.to_html(index=False, col_space='100px')
)
