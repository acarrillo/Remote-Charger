#!/usr/bin/env python -u

from socket import socket
import xml.etree.ElementTree as ET
import time
import sys

host = '128.36.14.59'
port = 80
path = "/lxi/infomation.xml" # NOTE THE MISSPELLING! This got me the first time around...but I later realized that the manufacturer misspelled the word "information."

last_voltage = '0.00'
last_set = 0
progBarTicks = 0
ticksToDraw = 0
progBarLen = 50

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

def updateProgressBar(lv):
    global progBarLen
    global progBarTicks
    for x in range(0,progBarLen+1+6): # Add 1 for end bracket, add 6 for voltage.
        sys.stdout.write('\b') # Flush.
    fracDone = float(lv)/4.2
    ticksToDraw = int(progBarLen*fracDone)
    spaceToDraw = progBarLen-ticksToDraw
    for x in range(0,ticksToDraw):
        sys.stdout.write('#') # Draw a tick.
        progBarTicks += 1
    for x in range(0,spaceToDraw):
        sys.stdout.write(' ') # Draw a space.
    sys.stdout.write(']') # Close prog bar.
    # Write voltage 
    sys.stdout.write(lv)
    sys.stdout.write("v")


#Initialize power supply
sys.stdout.write("Updating power supply settings")
connectServ('4097') # Press 'P25V' to select the P25V channel
sys.stdout.write('.')
connectServ('16449') # Press '4'
sys.stdout.write('.')
connectServ('16545') # Press '.'
sys.stdout.write('.')
connectServ('16417') # Press '2'
sys.stdout.write('.')
connectServ('12289') # Press 'V'
sys.stdout.write('.')

connectServ('16545') # Press '.'
sys.stdout.write('.')
connectServ('16465') # Press '5'
sys.stdout.write('.')
connectServ('12321') # Press 'A'
sys.stdout.write('.')

connectServ('8241') # Press 'ON' for P25V
sys.stdout.write('.\n')

# Do feedback loop
sys.stdout.write("Voltage [                                                  ]00.00v")
while float(last_voltage) < 4.2:
    xmldat = connectServ('0')
    try:
        root=ET.fromstring(xmldat)
        last_voltage = root[11].text
    except:
        pass # TODO: Debug why it occasionally fails
    updateProgressBar(last_voltage)
    #print "Read voltage\t\t",last_voltage

    time.sleep(1)
connectServ('8241') # Press 'OFF' for P25V
sys.stdout.write("\n")
print "Done! Killed the power supply."
