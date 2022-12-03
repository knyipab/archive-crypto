# Author: Ronald Yip
# First draft: Dec 2022
# Last update: Dec 2022
# Note: the response capture in implemented  with selenium-wire and indeed selenium better their BiDidirectional API for Python in the future

from seleniumwire import webdriver
from seleniumwire.webdriver import Chrome
import seleniumwire as selenium

import gzip
import zlib
import brotli

import warnings
import datetime
import re
import json
import time
from urllib.parse import urlparse
from urllib.parse import urljoin

class Browser(Chrome):
    def get(self, url: str):
        del self.requests
        if url[0:1] == '/' and re.search('[^:]+://.+', self.current_url):
            uri = urlparse(self.current_url)
            url = urljoin('{uri.scheme}://{uri.netloc}/'.format(uri=uri), url)
        return super().get(url)

    def retry(self, url: str, max_attempt: int = 4):
        try:
            r = self.get(url)
            return r
        except Exception as e:
            warnings.warn(str(e), stacklevel=2)
        raise Exception(f'retry failed for {url}')

    def retry_until_requests(self, url: str, pat: str = '', timeout: [int, float] = 20, max_attempt: int = 4, cooldown: int = 3, timeout_pow = 0.75, cooldown_pow = 2):
        for i in range(0, max_attempt):
            time.sleep(cooldown * (i ** cooldown_pow))
            try:
                self.get(url)
                r = self.wait_for_request(pat, timeout * ((i+1) ** timeout_pow))
                return r
            except Exception as e:
                warnings.warn(str(e), stacklevel=2)
        raise Exception(f'wait_for_request failed for {url}')
        
    def retry_until_no_request(self, url: str, pat: str = '', timeout: [int, float] = 20, timer: int = 2, max_attempt: int = 4, cooldown: int = 3, check_interval = 0.1, timeout_pow = 0.75, cooldown_pow = 2):
        for i in range(0, max_attempt):
            time.sleep(cooldown * (i ** cooldown_pow))
            self.get(url)
            start_time = datetime.datetime.now()
            while (datetime.datetime.now() - start_time).total_seconds() <= timeout * ((i+1) ** timeout_pow):
                r = ([None] + [r for r in self.requests if re.search(pat, r.url) and r.response and r.response.status_code < 300])[-1]
                if r and r.response and (datetime.datetime.now() - r.response.date).total_seconds() > timer:
                    return [r for r in self.requests if re.search(pat, r.url)]
                time.sleep(check_interval)
            warnings.warn(f'Timed out after {timeout * ((i+1) ** timeout_pow)}s waiting for request matching {pat}', stacklevel=2)
            
        raise Exception(f'retry_until_no_request failed for {url}')
    
    def archive_mhtml(self, filename):
        with open(filename, 'wb') as f:
            f.write(bytes(self.execute_cdp_cmd('Page.captureSnapshot', {})['data'], 'utf-8'))

        
def summarize_response(r):
    decoder_map = {k: v.decompress for k,v in {'br': brotli, 'gzip': gzip, 'deflate': zlib}.items()}
    decoder = decoder_map.get(r.response.headers.get('content-encoding')) or (lambda _:_)
    charset = (re.search('charset=([^;]*)', r.headers.get('content-type') or '') or [None,'utf-8'])[1]
    decoded_response = None
    try:
        decoded_response = decoder(r.response.body).decode(encoding=charset)
    except Exception:
        warnings.warn(f'Error decoding response from {r.url}, original bytes used instead', stacklevel=2)
        decoded_response = str(r.response.body)
    return {'url': r.url, 'method': r.method, 'payload': r.body.decode(), 
          'status_code': r.response.status_code, 'response': decoded_response}

def archive_response(response, filename):
    cache = [summarize_response(r) for r in response] if type(response) == list else summarize_response(r)
    with open(filename, 'wb') as f:
        f.write(bytes(json.dumps(cache), 'utf-8'))

def alloc_browser(headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.headless = headless
    driver = webdriver.Chrome(options=options)
    driver.__class__ = Browser
    return driver



