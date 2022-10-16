import os

indeed_search_word = "+".join(os.getenv("SEARCH_WORD").lower().split(" "))
reed_search_word = "-".join(os.getenv("SEARCH_WORD").lower().split(" ")) + "-jobs"
