
#######
# MIM #
#######
import datetime
def archive(browser, wa, folder):
    name = 'MIM'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    responses = browser.retry_until_no_request('https://analytics.abracadabra.money/overview', '/api/', timeout=30, timer=10)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
    wa.archive_response(responses, '{}/{}-{}.json'.format(folder, name, time_str))
