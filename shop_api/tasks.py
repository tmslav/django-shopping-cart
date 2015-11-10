from __future__ import absolute_import
import pylibmc

from .utils import  AhCrawler
from django.conf import settings

from celery import shared_task

mc = pylibmc.Client([settings.CELERY_RESULT_BACKEND.split("//")[1].replace("/","")])

def hash_info(site_name,user,password):
    return str(abs(hash(site_name+user+password)))

@shared_task
def login(site_name,user_name,password):
    if site_name == 'ah.nl':
        crawler = AhCrawler()
        if not crawler.get_cookie():
            crawler.login(user_name,password)
            mc[hash_info(site_name,user_name,password)]=crawler.get_cookie()

@shared_task
def add_product(site_name,user_name,password,product_id):
    try:
        cookie = mc[hash_info(site_name,user_name,password)]
    except KeyError:
        login(site_name,user_name,password)
        cookie = mc[hash_info(site_name,user_name,password)]

    ret = AhCrawler.add_product(product_id,cookie)
    #cookie is expired
    if not ret:
        #create new cookie and and the product
        login(site_name,user_name,password)
        ret = AhCrawler.add_product(product_id,mc[hash_info(site_name,user_name,password)])
        return ret
    else:
        return ret




