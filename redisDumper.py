#!/usr/bin/env python

import requests
import argparse
import re

parser = argparse.ArgumentParser(description='Parses a page for references to urls beginning with /_partial and pulls the json configs of those into files')
parser.add_argument('--url', dest='url', default=None, help='Please provide the url of the page you wanna scrape for _partial-urls')
parser.add_argument('--format', dest='format', default='json', help='Please provide the format you want to get, defaults to json')
args = parser.parse_args()

urlList = parseForPartials(url)


if r.status_code == 200:
  f = open('/Users/floriandietrich/Dev/scrapeMv/dumps/sushibar368.json', 'w+')
  f.write(r.content)
  f.close()

def parseForPartials(url):
  response = requests.get(url)
  if r.status_code == 200:
