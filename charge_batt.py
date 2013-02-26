#!/usr/bin/env python

from socket import socket
import xml.etree.ElementTree as ET
import time

host = '128.36.14.59'
port = 80
path = "/lxi/infomation.xml"

last_voltage = 0
last_set = 0

def connectServ(message):
    s = socket()
    s.connect((host, port))
    s.send("POST %s HTTP/1.1\r\n" % path)
    s.send("Host: %s\r\n" % host)
    s.send("Content-Type: text/xml\r\n")
    s.send("Content-Length: %d\r\n\r\n" % len(message))
    s.send(message)
    data=""
    for line in s.makefile():
        #print line
        data += line
        s.close()
    result = data.split("\n")
    xmldat = result[7]
    return xmldat


while 1:
    xmldat = connectServ('0')
    #print xmldat,"\n"
    try:
        root=ET.fromstring(xmldat)
        last_voltage = float(root[11].text)
        last_set = float(root[14].text)
    except ExpatError:
        pass
    print "Read voltage\t\t",last_voltage
    print "Setpoint voltage\t",last_set

    time.sleep(1)
