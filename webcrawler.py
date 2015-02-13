#!/usr/bin/env python

import urllib2
from BeautifulSoup import BeautifulSoup

def crawl(stop):
    stopAddress = ""
    url = 'http://www.dublinbus.ie/en/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery='
    
    # GET DATA SOURCE
    # get data from Dublinbus website
    header = {'User-Agent': 'Mozilla/5.0'} # Needed to prevent 403 error on Wikipedia
    req = urllib2.Request(url + str(stop),headers=header)
    response = urllib2.urlopen(req)
    # Let's make soup!!
    soup = BeautifulSoup(response)

    ## GET BUS STOP ADDRESS ##
    span = soup.find(id="ctl00_FullRegion_MainRegion_ContentColumns_holder_RealTimeStopInformation1_lblStopAddress")
    
    if span:
        stopAddress = span.contents[0].string
        
    print stopAddress

    return stopAddress