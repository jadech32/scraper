#!/usr/bin/env python3

import requests
import time
import threading
import json
from classes.logger import Logger
from classes.cart import Cart
from classes.tools import Tools
import winsound


if __name__ == '__main__':
    session = requests.Session()

    lock = threading.Lock()
    tools = Tools()
    config = tools.load('config/config.json')
    log = Logger().log
    cart = Cart(session, lock)

    log('Initializing script..','info')

    # Small, Medium, Large, one size. If no neg keywords, keep list empty, i.e. [], NOT ['']

    t1 = threading.Thread(target=cart.add_to_cart, args=(['urkle', 'white'], [], ['a'], ['g']))
    t2 = threading.Thread(target=cart.add_to_cart, args=(['panel', 'navy'], [], ['one'], []))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    cart.backdoor()


