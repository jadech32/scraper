#!/usr/bin/env python3
import threading
import requests
from xmltodict import parse
import json
import re
import webbrowser
from classes.logger import Logger
from classes.tools import Tools
import time
from classes.proxies import Proxy
import winsound
import csv
import itertools

log = Logger().log
tools = Tools()
config = tools.load('config/config.json')

default_url = str(config['settings']['url'] + 'sitemap_products_1.xml')
rate = float(config['settings']['polling_rate'])
checkout_url = str(config['settings']['url'] + 'cart/')
checkout_url_og = str(config['settings']['url'] + 'cart/')
retries = int(config['settings']['no_retries'])
retries_count = 0
empty_warn = 0



class Cart:

    def __init__(self, session, lock):
        self.session = session
        self.lock = lock


    def add_to_cart(self,keywords,neg_keywords,size, neg_size):
        #print(self.session)
        proxy = Proxy()
        session = self.session
        sess = requests.session()

        lock = self.lock
        if not proxy.getProxy():
            global empty_warn
            if empty_warn == 0:
                log('Not using any proxies','yellow')
                empty_warn = 1
            response = session.get(default_url)

        else:
            current_proxy = proxy.getProxy()[proxy.countProxy()]
            #res = sess.get('http://ip-api.com/json', proxies=current_proxy)
            #print(res.json()['query'])
            response = session.get(default_url, proxies=current_proxy)
            if (response.status_code != 200):
                log("proxy banned.." + str(response.status_code),'info')



        try:
            data = parse(response.content)
            data = json.loads(json.dumps(data))
            data = data['urlset']['url']
        except:
            log('Sitemap not live, retrying..','error')
            time.sleep(rate)
            self.add_to_cart(keywords, neg_keywords, size, neg_size)
        #print(data)

        item_url = ''
        item_id = ''
        item_name = ''

        # Find item
        try:
            for item in data[1:]:
                if 'image:image' in item:  # Some objects dont have image:image
                    # print(item['image:image'])
                    if not neg_keywords:

                        if all(i in item['image:image']['image:title'].lower() for i in keywords):
                            log('Item found: ' + str(item['image:image']['image:title']), 'yellow')

                            item_url = item['loc']
                            log('Item URL: ' + str(item_url), 'yellow')
                            item_name = item['image:image']['image:title']
                            break;
                    else:
                        if all(i in item['image:image']['image:title'].lower() for i in keywords) and \
                                not any(value in item['image:image']['image:title'].lower() for value in neg_keywords):
                            log('Item found: ' + str(item['image:image']['image:title']), 'yellow')

                            item_url = item['loc']
                            log('Item URL: ' + str(item_url), 'yellow')
                            item_name = item['image:image']['image:title']
                            break;

        except:
            log('Sitemap not yet live, retrying...','error')
            time.sleep(rate)
            self.add_to_cart(keywords, neg_keywords, size, neg_size)

        if item_url=='':
            log('Item not found, retrying...','error')
            time.sleep(rate)
            global retries_count
            global retries
            retries_count += 1
            if retries_count < retries:
                self.add_to_cart(keywords, neg_keywords, size, neg_size)
        else:

            page = session.get(item_url+'.json')
            #page_data = parse(page.content)
            page_data = json.loads(page.text)
            global checkout_url
            global checkout_url_og
            for item in page_data['product']['variants']:
                #winsound.Beep(1500, 1000)
                for i in size:

                    if float(i):
                        if '.5' in i:
                            if all(i in item['title'].lower() for i in size) and not any(
                                            value in item['title'].lower() for value in neg_size):
                                log('Variant found for size ' + item['title'] + ': ' + str(item['id']), 'yellow')
                                item_id = item['id']
                                checkout_url += str(item_id) + ':1,'
                                break
                        else:
                            if '.5' not in item['title'].lower() and all(i in item['title'].lower() for i in size) and not any(value in item['title'].lower() for value in neg_size):
                                log('Variant found for size ' + item['title'] + ': ' + str(item['id']),'yellow')
                                item_id = item['id']
                                checkout_url += str(item_id) + ':1,'
                                break


    def backdoor(self):
        if checkout_url != checkout_url_og:
            log('Opening URL..','success')
            webbrowser.open_new_tab(checkout_url)

    def sitemaplivecheck(self):
        proxy = Proxy()
        session = requests.session()
        if not proxy.getProxy():
            resp = session.get(default_url, allow_redirects=True)
        else:
            current_proxy = proxy.getProxy()[proxy.countProxy()]
            resp = session.get(default_url, proxies=current_proxy, allow_redirects=True)

        if resp.status_code != 200:
            print(resp.url)
            log('Sitemap not live, retrying..', 'error')
            self.sitemaplivecheck()
        else:
            print(resp.url)
            log('Sitemap is live!', 'success')
            return True

