#!/usr/bin/env python

from socket import socket
import xml.etree.ElementTree as ET

host = '128.36.14.59'
port = 80
path = "/lxi/infomation.xml"
xmlmessage = "0"

s = socket()
s.connect((host, port))
s.send("POST %s HTTP/1.1\r\n" % path)
s.send("Host: %s\r\n" % host)
s.send("Content-Type: text/xml\r\n")
s.send("Content-Length: %d\r\n\r\n" % len(xmlmessage))
s.send(xmlmessage)
data=""
for line in s.makefile():
    data += line
    s.close()
print data
#tree=ET.parse(
