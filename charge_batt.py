#!/usr/bin/env python

import urllib, urllib2

url = "http://128.36.14.59/lxi/infomation.xml"

data=urllib.urlencode({'data':'0'})
req=urllib2.Request(url,data)
response=urllib2.urlopen(req)
print response.geturl()
print response.info()
page=response.read()
print page
