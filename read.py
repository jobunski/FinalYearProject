#Rfid connection to Google Cloud IoT

import json
import sys
import socket
import RPi.GPIO as GPIO
from colors import bcolors
from mfrc522 import SimpleMFRC522

ADDR = '10.5.48.57'
PORT = 10000
# Create a UDP socket
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (ADDR, PORT)

device_id = sys.argv[1]
if not device_id:
    sys.exit('The device id must be specified.')

print('Bringing up device {}'.format(device_id))

def SendCommand(sock, message):
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendto(message, server_address)

    # Receive response
    print >>sys.stderr, 'waiting for response'
    response, _ = sock.recvfrom(4096)
    print >>sys.stderr, 'received: "%s"' % response

    return response

print ('Bring up device')

def MakeMessage(device_id, action, data=''):
    if data:
        return '{{ "device" : "{}", "action":"{}", "data" : "{}" }}'.format(device_id, action, data)
    else:
        return '{{ "device" : "{}", "action":"{}" }}'.format(device_id, action)

def RunAction(action, data=''):
    message = MakeMessage(device_id, action, data)
    if not message:
        return
    print('Send data: {} '.format(message))
    event_response = SendCommand(client_sock, message)
    print ("Response " + event_response)

reader = SimpleMFRC522()

try:
    RunAction('attach')
    RunAction('detach')
    RunAction('subscribe')

    id, text = reader.read()
    sys.stdout.write('\r >>' + bcolors.CGREEN + bcolors.BOLD +
                     'id: {}, Text: {}'.format(id, text) + bcolors.ENDC + ' <<')
    sys.stdout.flush()

    message = MakeMessage(device_id, 'event',
                          'id={}, text={}'.format(id, text))

    SendCommand(client_sock, message, False)

finally:
    print >> sys.stderr, "closing socket"
    GPIO.cleanup()

