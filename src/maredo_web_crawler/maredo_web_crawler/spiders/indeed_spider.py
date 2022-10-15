from typing import Optional, List, Dict

import scrapy


class IndeedJobsSpider(scrapy.Spider):
    name: Optional[str] = "indeed"
    base_url = "https://uk.indeed.com"
    allowed_domains = ['uk.indeed.com']
    search_string = "jobs?q=kyc+analyst&fromage=7&vjk=c334747f2048ad19"
    # handle_httpstatus_list = [400, 403, 404]
    paginator = 1
    incrementer = 0

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
        }
        urls = [
            f"{self.base_url}/{self.search_string}"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response, **kwargs):
        feedback = response.xpath('//h2[@class="jobTitle jobTitle-newJob css-bdjp2m eu4oa1w0"]')
        print(len(feedback))
        for record in feedback:
            print(record.attrib)
        # hrefs = (f"{self.base_url}" + link.attrib.get("href") for link in feedback)
        # print("================================================")
        # for idx, link in enumerate(hrefs, start=1):
        #     yield {
        #         "S/N": idx if self.incrementer < len(feedback) else idx + self.incrementer,
        #         "Job URL": link
        #     }
        # self.incrementer += len(feedback)

        # self.paginator += 1  # this increments for each recursive call to self.parse(*args, **kwargs)
        # has_next_page = response.xpath('//*[@id="nextPage"]/span/span/text()').get()
        # if has_next_page is not None:
        #     next_page = f"{self.base_url}/{self.search_string}&pageno={self.paginator}"
        #     print(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
