
#######
# DAI #
#######
import datetime
import pandas as pd
import json
def archive(browser, wa, folder):
    name = 'DAI'
    time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    responses = browser.retry_until_no_request('https://tracker-vaults.makerdao.network', '/data/', timeout=15, timer=3)
    browser.archive_mhtml('{}/{}-{}.mhtml'.format(folder, name, time_str))
    collateral_table = pd.DataFrame(json.loads(wa.summarize_response(responses[0])['response'])['data']['collaterals'])
    try:
        #for pathname in collateral_table['COLLATERAL'].str.extract('href="([^"]*)"')[0].to_list():
        #    responses += browser.retry_until_no_request(pathname, '/data/', timeout=10, timer=3)
    finally:
        wa.archive_response(responses, '{}/{}-{}.json'.format(folder, name, time_str))
