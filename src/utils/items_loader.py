import os
from pathlib import Path

import pandas as pd

from stmp_server import SendMultipartEmail
from config import recipients, title

reed_jobs = Path(__file__).parent.parent / "maredo_web_crawler/reed_jobs.json"
print(reed_jobs)
data = pd.read_json(reed_jobs)

print(data)

SendMultipartEmail(
    subject=f'{title} Reed Jobs',
    sender='wale.adekoya@btinternet.com',
    recipients=recipients,
    attachment_body=data.to_html(index=False, col_space='100px')
)

reed_jobs.unlink()
