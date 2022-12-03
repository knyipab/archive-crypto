
########
# USDN #
########
# data stored as string in requests
import datetime
import time
def archive(browser, wa, folder):
    name = 'USDN'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    browser.retry('https://neutrino.at/stats')
    time.sleep(10)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
