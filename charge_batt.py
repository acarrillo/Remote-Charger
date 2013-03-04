#!/usr/bin/env python -u

from socket import socket
import xml.etree.ElementTree as ET
import time
import sys
import signal

host_prefix = '128.36.14.'
port = 80
path = "/lxi/infomation.xml" # NOTE THE MISSPELLING! This got me the first time around...but I later realized that the manufacturer misspelled the word "information."
host = host_prefix + (sys.argv[1] if len(sys.argv) > 1 else '36')

last_voltage = '0.00'
last_current = '0.50'
progBarTicks = 0
ticksToDraw = 0
progBarLen = 50

# State booleans
atVoltageSetpoint = 0
atCurrMin = 0

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

def updateProgressBar(lv,lc):
    global progBarLen
    global progBarTicks
    for x in range(0,progBarLen+1+6+4+6+1+1): # Add 1 for end bracket, add 6 for voltage, add 4 for spacing, add 6 for current, add 1 for end paren.
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

    # Write current
    sys.stdout.write("    (")
    sys.stdout.write(lc)
    sys.stdout.write("A)")


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

# Do feedback loop to reach voltage setpoint
sys.stdout.write("Voltage [                                                  ]00.00v    (00.00A)") #Initialize progress bar
while not atVoltageSetpoint or not atCurrMin:
    try:
        xmldat = connectServ('0')
        try:
            root=ET.fromstring(xmldat)
            last_voltage = root[11].text
            last_current = root[12].text

            atVoltageSetpoint = float(last_voltage) >= 4.2 # Voltage setpoint is 4.2v
            atCurrMin = float(last_current) <= 0.035 # Current dropoff should not dip below 7% of current limit, or 35mA
        except:
            sys.stdout.write("\007")
            pass # TODO: Debug why it occasionally fails
        updateProgressBar(last_voltage,last_current)
        time.sleep(1)
    except KeyboardInterrupt:
        print "\nQuitting gracefully"
        break

connectServ('8241') # Press 'OFF' for P25V
sys.stdout.write("\n")
print "Done! Killed the power supply."
