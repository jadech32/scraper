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

    t1 = threading.Thread(target=cart.add_to_cart, args=(['urkle','knit','white'],            [],       ['small']))
    t2 = threading.Thread(target=cart.add_to_cart, args=(['line', 'stripe', 'white', 'shirt'], [], ['small']))
    t3 = threading.Thread(target=cart.add_to_cart, args=(['line','stripe','black','shirt'],   [],       ['small']))
    t4 = threading.Thread(target=cart.add_to_cart, args=(['line','crew','white'],             [],       ['small']))
    t5 = threading.Thread(target=cart.add_to_cart, args=(['6','panel','beige'],           ['pj','ldn'],       ['one']))
    t6 = threading.Thread(target=cart.add_to_cart, args=(['6','panel','navy'],         ['pj','ldn','correct'],       ['one']))
    t7 = threading.Thread(target=cart.add_to_cart, args=(['getting','higher','grey'],         [],       ['small']))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    cart.backdoor()
