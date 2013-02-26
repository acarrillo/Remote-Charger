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

#Initialize power supply
connectServ('4097') # Press 'P25V' to select the P25V channel
connectServ('16449') # Press '4'
connectServ('16545') # Press '.'
connectServ('16417') # Press '2'
connectServ('12289') # Press 'V'

connectServ('16545') # Press '.'
connectServ('16465') # Press '5'
connectServ('12321') # Press 'A'

connectServ('8241') # Press 'ON' for P25V

# Do feedback loop
while last_voltage < 4.2:
    xmldat = connectServ('0')
    #print xmldat,"\n"
    try:
        root=ET.fromstring(xmldat)
        last_voltage = float(root[11].text)
        last_set = float(root[14].text)
    except:
        pass # TODO: Debug why it occasionally fails
    print "Read voltage\t\t",last_voltage
    print "Setpoint voltage\t",last_set

    time.sleep(1)
connectServ('8241') # Press 'ON' for P25V
