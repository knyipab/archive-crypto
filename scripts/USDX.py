
########
# USDX #
########
# amounts are stored in 8 decimal places
# interpretation of collateral amount vs USDX issuance is tricky, may have to ask on Discord
import datetime
import time
def archive(browser, wa, folder):
    name = 'USDX'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    responses = browser.retry_until_no_request('https://app.kava.io/mint', 'api.{1,2}kava', timeout=30, timer=5)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
    wa.archive_response(responses, '{}/{}-{}.json'.format(folder, name, time_str))
