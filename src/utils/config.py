import os

indeed_search_word = "+".join(os.getenv("SEARCH_WORD").lower().split(" "))
reed_search_word = "-".join(os.getenv("SEARCH_WORD").lower().split(" ")) + "-jobs"

search_word = "_".join(os.getenv("SEARCH_WORD").lower().split(" "))
title = " ".join([s.capitalize() for s in os.getenv("SEARCH_WORD").split(" ")])

recipients = 'chezyfive@yahoo.com,wale.adekoya@btinternet.com'
if "kyc" in search_word or 'aml' in search_word or 'compliance' in search_word:
    recipients += ',favour.adekoya@yahoo.com'
