import requests
import re
import json

from urllib import quote,quote_plus
from urlparse import urljoin
from copy import deepcopy
import time
import os

def o(text):
    with open("temp.html","w") as f:
        f.write(text)
    print os.path.abspath("temp.html")

def current_milli_time():
    return int(round(time.time() * 1000))

login_headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"en-US,en;q=0.8,hr;q=0.6",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Pragma":"no-cache",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
}

cart_headers = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
            "Cache-Control":"no-cache",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "Pragma":"no-cache",
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2566.0 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest"
}

class BaseCrawler:
    def __init__(self):
        self.login_cookie = None

    def get_cookie(self):
        return self.login_cookie

class JumboCrawler(BaseCrawler):
    base_url = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewUserAccount-ViewLoginStart"

    form_login ="SynchronizerToken={}&ShopLoginForm_Login={}&ShopLoginForm_Password={}&login=Login"

    form_login_url = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewUserAccount-ProcessLogin"

    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
        "Cache-Control":"no-cache",
        "Connection":"keep-alive",
        "Content-Type":"application/x-www-form-urlencoded",
        "Pragma":"no-cache",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2566.0 Safari/537.36"
    }
    domain = "https://www.jumbo.com"

    @staticmethod
    def add_product(product, user_cookie,quantity=1):
        cookie,token = user_cookie
        post_url = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewCart-AddProductAjax"
        headers = deepcopy(cart_headers)
        headers["SynchronizerToken"] = token

        data = "SynchronizerToken={}&SKU={}&Quantity_{}={}&Unit_{}=&type=POST".format(
            quote(token),product,product,quantity,product)
        res = requests.post(post_url,data=data,headers=headers,cookies=cookie)
        if res.status_code==200:
            return True
        else:
            return False

    def login(self, user_name, password):
        #navigate to page
        res1 = requests.get(self.base_url)
        token = re.findall("SYNCHRONIZER_TOKEN_VALUE.=.\'(.*)\'",res1.text)[0]
        sid = re.findall("sid=(.*?);",res1.headers['Set-Cookie'])[0]
        pgid = re.findall("Site=(.*?);",res1.headers['Set-Cookie'])[0]

        first_req = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewSlotBooking-Countdown;pgid={};sid={}".format(pgid,sid)
        first_req_headers = {
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "*/*",
            "SynchronizerToken": token,
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2566.0 Safari/537.36",
            "Referer": self.base_url,
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8,hr;q=0.6,es;q=0.4,zh;q=0.2,ja;q=0.2",
            "Cookie": "sid={}; pgid-Jumbo-Grocery-Site={}".format(sid,pgid)
        }
        first_res = requests.get(first_req,headers = first_req_headers)
        sec_req = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewCart-ShowMiniBasket;pgid={};sid={}".format(pgid,sid)
        sec_res = requests.get(sec_req,headers=first_req_headers)

        #post to login start
        login_url = "https://www.jumbo.com/INTERSHOP/web/WFS/Jumbo-Grocery-Site/nl_NL/-/EUR/ViewUserAccount-ProcessLogin;pgid={};sid={}".format(pgid,sid)
        form_login = self.form_login.format(quote(token),quote(user_name),quote(password))

        redirect = requests.post(login_url,data=form_login,headers=self.headers,cookies = res1.cookies,allow_redirects=False)
        res = requests.get(urljoin(login_url,redirect.headers['Location']),headers = self.headers,cookies=redirect.cookies)
        ret_cookies = {}
        for k,v in redirect.cookies.get_dict().iteritems():
            ret_cookies[k]=v
        for k,v in res1.cookies.get_dict().iteritems():
            ret_cookies[k]=v
        self.login_cookie = (ret_cookies,token)

class AhCrawler(BaseCrawler):
    form_data = "userName={}&password={}&rememberUser=true"

    base_url = "https://www.ah.nl/mijn/inloggen/basis?ref=http://www.ah.nl/"

    domain = "https://www.ah.nl/"

    headers = deepcopy(login_headers)
    headers["Content-Type"] = "application/x-www-form-urlencoded"

    @staticmethod
    def add_product(product_id, user_cookie,quantity=1):
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

        product_pattern = '{"type":"PRODUCT","item":{"id":":product_id"},"quantity":":quantity","originCode":"BON"}'
        post_data = product_pattern.replace(":product_id", product_id).replace(":quantity",str(quantity))

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

class HoogvlietCrawler(BaseCrawler):
    login_url = "https://www.hoogvliet.com/inloggen"
    login_post_url = "https://www.hoogvliet.com/INTERSHOP/web/WFS/org-webshop-Site/nl_NL/-/EUR/ViewUserAccount-ProcessLogin"

    def login(self,user_name,password):
        session = requests.Session()
        headers= deepcopy(login_headers)
        login_page = session.get(self.login_url,headers=headers)
        headers["Content-Type"]="application/x-www-form-urlencoded"
        token = re.findall("SYNCHRONIZER_TOKEN_VALUE.=.\'(.*)\'",login_page.text)[0]
        post_data = "SynchronizerToken={}&ShopLoginForm_Login={}&ShopLoginForm_Password={}&login=Login".format(quote(token),quote(user_name),quote(password))
        redirect = session.post(self.login_post_url,headers=headers,data=post_data)
        self.login_cookie = deepcopy((session.cookies,token))

    @staticmethod
    def add_product(product,cookie,quantity=1):
        url = "https://www.hoogvliet.com/INTERSHOP/web/WFS/org-webshop-Site/nl_NL/-/EUR/ViewCart-AddProduct"
        cookie,token = cookie
        headers = deepcopy(cart_headers)
        headers['SynchronizerToken'] = token
        post_data = "SynchronizerToken={}&urlAction=https%3A%2F%2Fwww.hoogvliet.com%2FINTERSHOP%2Fweb%2FWFS%2Forg-webshop-Site%2Fnl_NL%2F-%2FEUR%2FViewCart-AddProduct&Quantity_{}={}&SKU={}".format(token,product,quantity,product)
        res = requests.post(url,data=post_data,cookies=cookie,headers=headers)
        if res.status_code == 200:
            return True
        else:
            return False

class CooponlineCrawler(BaseCrawler):
    login_url = "https://www.cooponline.nl/cooponline/api/login.cfm"
    add_product_url = "https://api-01.cooponline.nl/shopapi/basket/add/{}/{}/true/{}" #product_id,quantity,basket


    @staticmethod
    def add_product(product,user_cookie,quantity=1):
        cookie,token,basket = user_cookie
        headers = deepcopy(login_headers)
        headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        headers['Content-Type'] ="application/x-www-form-urlencoded; charset=UTF-8"
        del headers["Upgrade-Insecure-Requests"]
        post_body = "token={}&ie_fix={}".format(token,current_milli_time())
        res = requests.post(CooponlineCrawler.add_product_url.format(product,quantity,basket),data=post_body,headers=headers,cookies=cookie.get_dict())
        if json.loads(res.text)['status'] == 'OK':
            return True
        else:
            return False


    def login(self,user_name,password):
        session = requests.Session()
        session.get("https://www.cooponline.nl",headers=login_headers)
        post_data = "username={}&password={}&checklogin=1&currentUrl=https%3A%2F%2Fwww.cooponline.nl%2F&passwordRecoveryUsername=".format(quote(user_name),password)
        headers = deepcopy(login_headers)
        headers['Content-Type'] = "application/x-www-form-urlencoded"
        login_page = session.post(self.login_url,headers=headers,data=post_data)
        token = re.findall("token.*?\'(.*?)\'",login_page.text)[0]
        basket_id = re.findall("basket/countItems/(.*?)\"",login_page.text)[0]

        self.login_cookie = deepcopy((session.cookies,token,basket_id))

#class PlusCrawler(BaseCrawler):
#    login_url = "https://www.plus.nl/inloggen"
#    proces_login_url = "https://www.plus.nl/INTERSHOP/web/WFS/PLUS-website-Site/nl_NL/-/EUR/ViewUserAccount-ProcessLogin"
#
#    def login(self,user_name,password):
#        session = requests.Session()
#        login_page = session.get(self.login_url,headers=self.login_headers)
#        token = re.findall("SynchronizerToken.*?value..(.*?)\"",login_page.text)[0]
#        test=session.get("https://www.plus.nl/INTERSHOP/web/WFS/PLUS-website-Site/nl_NL/-/EUR/GetExternalizedStrings-Start",headers = self.cart_headers)
#        cart=session.post("https://www.plus.nl/INTERSHOP/web/WFS/PLUS-website-Site/nl_NL/-/EUR/ViewMiniCart-Start",data="",headers=self.cart_headers)
#        post_data = "SynchronizerToken={}&ShopLoginForm_Login={}&ShopLoginForm_Password={}&login=Login".format(quote(token),quote(user_name),quote(password))
#        process_login = session.post(self.proces_login_url,data = post_data,headers=self.login_headers,allow_redirects=False)
#        import ipdb;ipdb.set_trace()
#        self.login_cookie = (session.cookies,token)
#
#    @staticmethod
#    def add_product(product,user_cookie):
#        pass

class Crawler(object):
    classes = {
        'ah.nl': AhCrawler,
        'jumbo.com': JumboCrawler,
        #        'plus.nl':PlusCrawler,
        'hoogvliet.com':HoogvlietCrawler,
        'cooponline.nl':CooponlineCrawler
    }
    @staticmethod
    def add_product(site_name,product, user_cookie,quantity):
        return Crawler.classes[site_name].add_product(product,user_cookie,quantity)

    def __new__(cls, *args, **kwargs):
        cls.add_product = cls.classes[args[0]].add_product
        return cls.classes[args[0]]()
