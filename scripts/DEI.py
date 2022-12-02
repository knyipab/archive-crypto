    
#######
# DEI #
#######
# data stored as in hexadecimal string (rpc.ftm.tools)
import datetime
import time
def archive(browser, wa, folder):
    name = 'DEI'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    browser.get('https://app.dei.finance/dashboard')
    time.sleep(10)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
