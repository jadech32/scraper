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
log = Logger().log
tools = Tools()
config = tools.load('config/config.json')

default_url = str(config['settings']['url'] + 'sitemap_products_1.xml')
rate = float(config['settings']['polling_rate'])
checkout_url = str(config['settings']['url'] + 'cart/')
checkout_url_og = str(config['settings']['url'] + 'cart/')
retries = int(config['settings']['no_retries'])
retries_count = 0

class Cart:

    def __init__(self, session, lock):
        self.session = session
        self.lock = lock

    def add_to_cart(self,keywords,size):
        #print(self.session)
        session = self.session
        lock = self.lock

        response = session.get(default_url)

        data = parse(response.content)
        data = json.loads(json.dumps(data))
        data = data['urlset']['url']
        #print(data)

        item_url = ''
        item_id = ''
        item_name = ''

        # Find item
        for item in data[1:]:
            if 'image:image' in item: # Some objects dont have image:image
                #print(item['image:image'])

                if all(i in item['image:image']['image:title'].lower() for i in keywords):
                    log('Item found: ' + str(item['image:image']['image:title']),'yellow')

                    item_url = item['loc']
                    item_name = item['image:image']['image:title']
                    break;

        if item_url=='':
            log('Item not found, retrying...','error')
            time.sleep(rate)
            global retries_count
            global retries
            retries_count += 1
            if retries_count < retries:
                self.add_to_cart(keywords,size)
        else:
            page = session.get(item_url+'.json')
            #page_data = parse(page.content)
            page_data = json.loads(page.text)
            global checkout_url
            global checkout_url_og
            for item in page_data['product']['variants']:
                if(size.lower() == item['title'].lower()):
                    log('Variant found for size ' + item['title'] + ': ' + str(item['id']),'yellow')
                    item_id = item['id']
                    checkout_url = checkout_url + str(item_id) + ':1,'
                    break;

        if checkout_url != checkout_url_og:
            self.backdoor()
    def backdoor(self):
        webbrowser.open_new_tab(checkout_url)
