import time
def fitch_headlines():
    URL = "https://www.fitchratings.com/api/v2/headlines?limit=20&offset=0&_={}"
    now_time = str(int(time.time()*1000))
    yield URL.format(now_time)

