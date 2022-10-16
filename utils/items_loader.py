from pathlib import Path

import pandas as pd

from stmp_server import SendMultipartEmail

reed_jobs = Path(__file__).parent.parent / "src/maredo_web_crawler/reed.json"

data = pd.read_json(reed_jobs)

print(data)

SendMultipartEmail(
    subject='KYC Analyst Reed Jobs',
    sender='wale.adekoya@btinternet.com',
    recipients='chezyfive@yahoo.com,favour.adekoya@yahoo.com,wale.adekoya@btinternet.com',
    attachment_body=data.to_html(index=False, col_space='100px')
)

reed_jobs.unlink()
