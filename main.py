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

def main():
    browser = wa.alloc_browser(False)
    sfolder = './scripts'
    archive_folder = './archive/' + datetime.datetime.now().strftime('%Y%m')
    os.makedirs(archive_folder, exist_ok=True)
    packages = [f.split('.')[0] for f in os.listdir(sfolder) if os.path.isfile(os.path.join(sfolder, f))]
    modules = {p: importlib.import_module(sfolder.split('/')[-1] + '.' + p) for p in packages}
    error = None
    for name, module in modules.items():
        try:
            if hasattr(module, 'archive'):
                module.archive(browser, wa, archive_folder)
        except Exception as e:
            traceback.print_exc()
            error = e
    browser.get('https://www.coingecko.com/en/categories/stablecoins')
    df_top_stablecoins = pd.read_html(browser.page_source)[0].eval("mktcap = `Market Capitalization`.replace('[^0-9]','',regex=True).replace('','0').astype('int')")
    above_75mil = df_top_stablecoins.query("mktcap > 75000000").eval("Coin.str.split(' ').str[-1]").to_list()
    browser.quit()
    if not set(above_75mil).issubset(set(packages)): raise Exception(f'{set(above_75mil) - set(packages)} has market cap of $75mil+ but missing')
    if error: raise Exception('Exception in archiving. See warnings. ')

if __name__ == "__main__":
    main()


