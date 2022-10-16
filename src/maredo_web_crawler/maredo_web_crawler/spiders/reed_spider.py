import pathlib
import sys
from typing import Optional

import scrapy

sys.path.append(pathlib.Path(__file__).parent.parent.parent.parent.parent.__str__())


class ReedSpider(scrapy.Spider):
    name: Optional[str] = "reed"
    base_url = "https://www.reed.co.uk"
    search_string = "jobs/kyc-jobs?datecreatedoffset=LastWeek"
    paginator = 1
    incrementer = 0

    # start_urls: Optional[List[str]] = [
    #     "https://www.reed.co.uk/jobs/kyc-jobs?datecreatedoffset=LastWeek"
    # ]

    def start_requests(self):
        urls = [
            f"{self.base_url}/{self.search_string}"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        feedback = response.xpath('//h3/a[@href]')
        print(len(feedback))
        print("================================================")
        for idx, link in enumerate(feedback, start=1):
            yield {
                "S/N": idx if self.incrementer < len(feedback) else idx + self.incrementer,
                'Title': link.attrib.get("title"),
                "Url": f"{self.base_url}" + link.attrib.get("href"),
            }
        self.incrementer += len(feedback)

        self.paginator += 1  # this increments for each recursive call to self.parse(*args, **kwargs)
        has_next_page = response.xpath('//*[@id="nextPage"]/span/span/text()').get()
        if has_next_page is not None:
            next_page = f"{self.base_url}/{self.search_string}&pageno={self.paginator}"
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
