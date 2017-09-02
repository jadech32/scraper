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
import csv
import itertools
log = Logger().log

class Proxy:

    def __init__(self):
        self.proxies = self.importProxy()
        self.countOG = len(self.proxies) - 1
        self.count = len(self.proxies) - 1

    def importProxy(self):
        results = []
        with open('config/proxies.txt', newline='') as inputfile:
            for row in csv.reader(inputfile):
                results.append(row)

        return list(map(lambda x: {'https': 'https://'+x}, list(itertools.chain.from_iterable(results))))

    def getProxy(self):
        return self.proxies

    def countProxy(self):
        if self.count == 0:
            self.count = self.countOG
        else:
            self.count = self.count - 1
        return self.count

