#!/usr/bin/env python

import sys
import requests
import argparse
import re
import json
import os
from urlparse import urlparse

parser = argparse.ArgumentParser(description='Parses a page for references to urls beginning with /_partial and pulls the json configs of those into files')
parser.add_argument('--url', dest='url', default=None, help='Please provide the url of the page you wanna scrape for _partial-urls')
parser.add_argument('--format', dest='format', default='json', help='Please provide the format you want to get, defaults to json')
args = parser.parse_args()

# some regex for parsing
partialRegex = '(?P<url>/_partial/[^/]+/[^"]+)'
partsRegex = '/_partial/(?P<type>[^/]+)/(?P<id>\d+)'

# some parameters
requestUrl = urlparse(args.url)
baseUrl = requestUrl.scheme + '://' + requestUrl.netloc
print 'Base-URL: ' + baseUrl

# output
baseDir = os.path.dirname(os.path.realpath(__file__))
print 'Base Directory:  ' + baseDir

outputDir = os.path.join(baseDir, 'dumps')
print 'Output Directory: ' + outputDir

if not os.path.exists(outputDir):
    os.makedirs(outputDir)
    print 'Output-Directory does not exist. Creating.'

# parse the html-response for partial urls
def parseForPartials(url):
    response = requests.get(url)

    if response.status_code == 200:
        matches = re.findall(partialRegex, response.content)

        if matches:
            return matches
        else:
            print 'No partials found. Aborting.'
            sys.exit(1)

# parse the partial urls to construct filepaths
def parseRequestUrl(url):
    matches = re.search(partsRegex, url)

    if matches:
        matches = matches.groupdict()
        return matches
    else:
        print 'Partial Url: ' + url + 'has no known format'

# save a text string to an ordered json file
def saveJsonFile(filename, content):
    outputPath = os.path.join(outputDir, filename)
    print 'Writing output to ' + outputPath

    jsonObj = json.loads(content)

    with open(outputPath, 'w+') as outfile:
        json.dump(jsonObj, outfile, sort_keys=True, indent=4)

urlList = parseForPartials(args.url)
print 'Found following partial urls on ' + args.url + ': \n' + '\n'.join(urlList)

for url in urlList:
    # get info for filename
    urlParts = parseRequestUrl(url)

    #build request
    payload = {'_format': args.format}
    response = requests.get(baseUrl + url, params=payload)

    if response.status_code == 200:
            filename = ''.join([urlParts['type'], urlParts['id'], '.json'])
            # print 'TargetFilename: ' + filename
            saveJsonFile(filename, response.text)
    else:
        print response.status_code
        sys.exit(0)


