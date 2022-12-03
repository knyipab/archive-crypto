
########
# OUSD #
########
# unknown site of analytics, perhaps main page?
import datetime
import time
def archive(browser, wa, folder):
    name = 'OUSD'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    browser.retry('https://www.ousd.com/')
    time.sleep(10)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
