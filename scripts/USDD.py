
########
# USDD #
########
# data trasmitted through websocket, so only mhtml captured
import datetime
import time
def archive(browser, wa, folder):
    name = 'USDD'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    browser.retry('https://tdr.org/')
    time.sleep(10)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
