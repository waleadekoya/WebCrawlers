import os
from pathlib import Path

import pandas as pd

from stmp_server import SendMultipartEmail

search_word = "_".join(os.getenv("SEARCH_WORD").lower().split(" "))
title = " ".join([s.capitalize() for s in os.getenv("SEARCH_WORD").split(" ")])

reed_jobs = Path(__file__).parent.parent / "maredo_web_crawler/reed_jobs.json"
print(reed_jobs)
data = pd.read_json(reed_jobs)

print(data)

recipients = 'chezyfive@yahoo.com,wale.adekoya@btinternet.com'
if "kyc" in search_word or 'aml' in search_word or 'compliance' in search_word:
    recipients += ',favour.adekoya@yahoo.com'

SendMultipartEmail(
    subject=f'{title} Reed Jobs',
    sender='wale.adekoya@btinternet.com',
    recipients=recipients,
    attachment_body=data.to_html(index=False, col_space='100px')
)

reed_jobs.unlink()
