import socket
import select
import traceback
import netifaces

# [MAGIC(2) | TYPE(1) | LENGTH(1) | CONTENT(LENGTH)]
# MAGIC: 0x29 0xad
# TYPE: 0 => discovery broadcast
#       1 => set private info
#       2 => master server
#       3 => room controller
#       4 => TV controller
#       5 => camera

PORT = 9291
HOSTS = []
IP_PREFIXES = ["192.168.", "10.10."]
BUFFERS = {}
CALLBACKS = {}

try: #disable stdout i/o buffering
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
except: pass

def find_hosts():
  global HOSTS
  HOSTS = []
  for i in netifaces.interfaces():
    try:
      ip = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
      for pre in IP_PREFIXES:
        if pre in ip:
          HOSTS += [ip]
          break
    except: pass

def OpenHostingSockets():
  find_hosts()

  sarr = []
  for h in HOSTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("",PORT))
    sarr += [s]
    break
  return sarr

def OpenBroadcastSocket():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
  return s

def GetBroadcastAddress():
  return ('<broadcast>', PORT)

def OnInput(message, address):
  try:
    BUFFERS[address] += message
  except:
    BUFFERS[address] = message
  msg = bytearray(list(BUFFERS[address]))
  while len(msg) >= 4:
    if msg[0] == 0x29 and msg[1] == 0xad:
      # an actual broadcast!
      size = int(msg[3])
      if len(msg) >= 4 + size:
        # we have the full packet!
        try:
          CALLBACKS[str(msg[2])](address, msg[2], msg[3], msg[4:])
        except: pass
        msg = msg[int(size)+4:]
      else:
        break # wait for more input
    else:
      msg = msg[1:]
  BUFFERS[address] = msg

def SetCallback(types, f):
  for t in types:
    CALLBACKS[str(t)] = f

def MakePacket(type, text):
  return bytearray([0x29, 0xad, type, len(text)]) + text.encode('UTF-8')

def MakeSettingsPacket(type, name):
  return MakePacket(1, bytearray([type]).decode()+name)

def SetSettings(ip, type, name):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.sendto(MakeSettingsPacket(type, name), (ip, PORT))
  s.close()
