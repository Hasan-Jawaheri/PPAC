import serial
import time
import requests
import json
import sys
import math

import socket
import traceback
import netifaces

from basicmath import *

sys.path.insert(0, '../debugger/discovery/')
import discovery

DEBUGGER_IP = '192.168.1.105'
DEBUGGER_PORT = 8000
DEBUGGER_LINK = 'setinfo/'

def cb_identifier(source, type, size, text):
  DEBUGGER_IP = str(source)
discovery.SetCallback([2, 3, 4, 5], cb_identifier)

while 1:
  try:
    s = discovery.OpenBroadcastSocket()
    s.sendto(discovery.MakePacket(0, ""), discovery.GetBroadcastAddress())
    message, address = s.recvfrom(100)
    discovery.OnInput(message, address)
    s.close()
    if DEBUGGER_IP:
      break
  except Exception as e:
    print str(e)

DEBUGGER_URL = 'http://'+DEBUGGER_IP+':'+str(DEBUGGER_PORT)+'/debug/'+DEBUGGER_LINK
print ("Debugger link: " + DEBUGGER_URL)

def sendDebugInfo(info):
  try:
    requests.post(DEBUGGER_URL, data = info)
  except Exception as e:
    print str(e)

initialization_timer = time.time()
pose_matrix = None
pose_inverse = None
current_matrix = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
motor_positions = [(-1, 0),
                   (-math.sin(30), math.cos(30)),
                   (math.sin(30), math.cos(30)),
                   (1, 0),
                   (-math.sin(30),-math.cos(30)),
                   (math.sin(30),-math.cos(30))]

def OnStateChange(cur_time, mtx):
  global pose_matrix, pose_inverse, current_matrix, motor_positions
  if pose_matrix == None:
    return

  new_matrix = MtxMultiply(mtx, pose_inverse)
  cur_motor_positions = []
  for p in motor_positions:
    (x, y)
    cur_motor_positions += [MtxVecMultiply(new_matrix, (x, 0, y, 1))]
  current_matrix = new_matrix

sp = None
serial_types = ["COM", "/dev/ttyUSB", "/dev/ttyACM", "/dev/cu.usbmodem141"]
serial_type = 3
serial_port = 0

while True:
  try:
    while True:
      try:
        sp = serial.Serial()
        sp.baudrate = 9600
        sp.port = serial_types[serial_type] + str(serial_port)
        sp.open()
        print ('Connected to Arduino on serial')
        time.sleep(1)
      except Exception as e:
        print ('Failed to initiate serial communication: ' + str(e))
        time.sleep(0.1)
        serial_port += 1
        if serial_port == 8:
          serial_port = 0
          serial_type = (serial_type + 1) % len(serial_types)
          if serial_type == 0 and serial_port < 2:
            serial_port = 2
        continue
      break

    print ("here we go...")
    sp.flushInput()
    sp_buffer = bytearray([])

    while True:
      while sp.inWaiting():
        b = sp.read()
        sp_buffer += b
        if b == "\n":
          break
      if len(sp_buffer) > 0:
        try:
          if "\n" in sp_buffer:
            i = sp_buffer.index('\n')
            if i > 0:
              info = str(sp_buffer[:i-1])
              info = info.split(',')
              if len(info) == 9:
                mtx = [float(info[0]), float(info[3]), float(info[6]),float(info[1]), float(info[4]), float(info[7]),float(info[2]), float(info[5]), float(info[8])]
                cur_time = time.time()
                if pose_matrix == None and cur_time - initialization_timer > 4:
                  pose_matrix = mtx
                  pose_inverse = MtxInverse(pose_mtx)
                  sendDebugInfo({'pose':json.dumps(pose_matrix)})
                sendDebugInfo({'matrix':json.dumps(mtx)})
                OnStateChange(cur_time, mtx)
            sp_buffer = sp_buffer[i+1:]
        except Exception as e:
          print (str(e))
          raise
  except Exception as e:
    print (str(e))

