#!/usr/bin/env python3

########
# main # 
########

import webarchive as wa
import warnings
import traceback
import os
import importlib
import pandas as pd
import datetime
import requests

def main():
    browser = wa.alloc_browser(not os.environ.get('DISPLAY'))
    sfolder = './scripts'
    archive_folder = datetime.datetime.now().strftime('./archive/%Y%m/%Y%m%d_%H')
    os.makedirs(archive_folder, exist_ok=True)
    packages = [f.split('.')[0] for f in os.listdir(sfolder) if os.path.isfile(os.path.join(sfolder, f))]
    modules = {p: importlib.import_module(sfolder.split('/')[-1] + '.' + p) for p in packages}
    exit_code = 0
    try:
        df_top_stablecoins = pd.DataFrame(requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=stablecoins&order=market_cap_desc&per_page=100&page=1&sparkline=false').json())
        above_75mil = df_top_stablecoins.query("market_cap > 75000000").eval('symbol.str.upper()').to_list()
        #browser.retry('https://www.coingecko.com/en/categories/stablecoins')
        #df_top_stablecoins = pd.read_html(browser.page_source)[0].eval("mktcap = `Market Capitalization`.replace('[^0-9]','',regex=True).replace('','0').astype('int')")
        #above_75mil = df_top_stablecoins.query("mktcap > 75000000").eval("Coin.str.split(' ').str[-1]").to_list()
        if not set(above_75mil).issubset(set(packages)):
            warnings.warn(f'{set(above_75mil) - set(packages)} has market cap of $75mil+ but missing')
            exit_code = 1
    except Exception as e:
        traceback.print_exc()
        exit_code = 1
    
    for name, module in modules.items():
        try:
            if hasattr(module, 'archive'):
                module.archive(browser, wa, archive_folder)
        except Exception as e:
            traceback.print_exc()
            exit_code = 1
    
    browser.quit()
    
    exit(exit_code)

if __name__ == "__main__":
    main()


