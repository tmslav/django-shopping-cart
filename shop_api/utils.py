import requests
import re

from urllib import quote
from urlparse import urljoin
from copy import deepcopy


class AhCrawler:
    form_data = "userName={}&password={}&rememberUser=true"

    base_url = "https://www.ah.nl/mijn/inloggen/basis?ref=http://www.ah.nl/"

    domain = "https://www.ah.nl/"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "www.ah.nl",
        "Origin": "https://www.ah.nl",
        "Pragma": "no-cache",
        "Referer": "https://www.ah.nl/mijn/inloggen/basis?ref=http://www.ah.nl/",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2560.0 Safari/537.36'
    }

    login_cookie = None

    @staticmethod
    def add_product(product_id, user_cookie):
        add_product_headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "www.ah.nl",
            "Origin": "http://www.ah.nl",
            "Pragma": "no-cache",
            "Referer": "http://www.ah.nl/bonus?ah_campaign=intern&ah_mchannel=ah&ah_source=homepage&ah_linkname=promolane-1-assortiment-bonus-2015.wk46",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2560.0 Safari/537.36",
            "X-Requested-With": 'XMLHttpRequest'
        }
        add_product_url = "http://www.ah.nl/service/rest/shoppinglists/0/items"

        product_pattern = '{"type":"PRODUCT","item":{"id":":product_id"},"quantity":1,"originCode":"BON"}'

        post_data = product_pattern.replace(":product_id", product_id)

        res = requests.post(add_product_url, data=post_data,
                                cookies=user_cookie, headers=add_product_headers)

        if res.status_code == 200:
            return True
        else:
            return False

    def login(self, user_name, password):
        res = requests.get(self.base_url)
        form_data = self.form_data.format(quote(user_name), quote(password))
        res = requests.post(self.base_url, data=form_data, cookies=res.cookies, headers=self.headers)

        next_url = re.findall("replace\(.(.*)\"", res.text)
        headers = deepcopy(self.headers)

        if next_url:
            next_url = urljoin(self.domain, next_url[0])
        else:
            raise Exception("Ah.nl - login failed");

        res = requests.get(next_url, cookies=res.cookies, headers=self.headers)

        headers['Referer'] = next_url

        next_url = re.findall("replace\(.(.*)\'", res.text)

        if next_url:
            next_url = urljoin(self.domain, next_url[0])
        else:
            raise Exception("Ah.nl - login failed");
        login_cookie = deepcopy(res.cookies)
        res = requests.get(next_url, cookies=res.cookies, headers=self.headers)

        headers['Referer'] = next_url

        next_url = re.findall("replace\(.(.*)\"", res.text)

        if next_url:
            next_url = urljoin(self.domain, next_url[0])
        else:
            raise Exception("Ah.nl - login failed");

        res = requests.get(next_url, cookies=login_cookie, headers=self.headers)

        self.login_cookie = login_cookie

    def get_cookie(self):
        return self.login_cookie
