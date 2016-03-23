import socket
import traceback
import netifaces
import discovery

def cb_identifier(source, type, size, text):
  print (source)
  print (type)
  print (text)
discovery.SetCallback([2, 3, 4, 5], cb_identifier)

s = discovery.OpenBroadcastSocket()
s.sendto(discovery.MakePacket(0, ""), discovery.GetBroadcastAddress())

try:
  while 1:
    message, address = s.recvfrom(100)
    discovery.OnInput(message, address)
finally:
  s.close()
