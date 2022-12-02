
########
# FRAX #
########
import datetime
def archive(browser, wa, folder):
    name = 'FRAX'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    responses = browser.retry_until_no_request('https://app.frax.finance/', 'api.frax', timeout=30, timer=8)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
    wa.archive_response(responses, '{}/{}-{}.json'.format(folder, name, time_str))
    name = 'FRAX_AMOs'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    responses = browser.retry_until_no_request('https://app.frax.finance/amos', 'api.frax', timeout=30, timer=8)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
    wa.archive_response(responses, '{}/{}-{}.json'.format(folder, name, time_str))
