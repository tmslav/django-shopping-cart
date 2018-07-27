from __future__ import absolute_import
import pylibmc

from .utils import  Crawler
from django.conf import settings

from celery import shared_task
from celery.contrib import rdb
from .models import ShopOrders,MemcachedKeys
from datetime import datetime, timedelta

mc = pylibmc.Client([settings.CELERY_RESULT_BACKEND.split("//")[1].replace("/","")])

def hash_info(site_name,user,password):
    return str(abs(hash(site_name+user+password)))


@shared_task
def clean_memcached():
    time_threshold = datetime.now() - timedelta(minutes=30)
    keys_objects = MemcachedKeys.objects.filter(last_used__lte=time_threshold)
    for k in keys_objects:
        try:
            del mc[k.key]
        except:
            pass


@shared_task
def login(site_name,user_name,password):
    crawler = Crawler(site_name)
    if not crawler.get_cookie():
        crawler.login(user_name,password)
        mc[hash_info(site_name,user_name,password)]=crawler.get_cookie()

@shared_task
def add_product(site_name,user_name,password,product_id,quantity):
    crawler = Crawler(site_name)
    try:
        cookie = mc[hash_info(site_name,user_name,password)]
    except KeyError:
        login(site_name,user_name,password)
        cookie = mc[hash_info(site_name,user_name,password)]
    ret = crawler.add_product(product_id,cookie,quantity)
    #cookie is expired
    if not ret:
        #create new cookie and and the product
        login(site_name,user_name,password)
        ret = crawler.add_product(product_id,mc[hash_info(site_name,user_name,password)],quantity)
        return ret
    else:
        return ret

@shared_task
def check_results(return_value,database_id):
    item = ShopOrders.objects.get(task_id=database_id)
    if return_value:
        item.task_status = 'D'
    else:
        item.task_status = 'F'
    item.save()



def test_all():
    print add_product("jumbo.com","tmslav@gmail.com","","134137FLS",5)
    print add_product("ah.nl","tmslav@gmail.com","","wi228467",5)
    print add_product("hoogvliet.com","tmslav@gmail.com","","025950000",5)
    print add_product("cooponline.nl","tmslav@gmail.com","","63502",5)


