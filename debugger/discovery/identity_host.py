import socket
import traceback
import netifaces
import time
import discovery
import select

def WriteIdentity():
  with open("identity", "w") as f:
    for d in mydesc:
      f.write(str(d[0]) + "\n")
      f.write(d[1] + "\n")
    f.close()
mydesc = [(3, "New Room")]
try:
  with open("identity", "r") as f:
      content = f.readlines()
      content = list(map(lambda x: x[:-1] if x[-1] == "\n" else x, content))
      if len(content) == 0 or len(content) % 2 != 0:
        raise
      mydesc = []
      for i in range(0, len(content), 2):
        mydesc += [(int(content[i]), str(content[i+1]))]
except:
  WriteIdentity()

discovery.find_hosts()
print ("Hosting on %s:%d" % (discovery.HOSTS, discovery.PORT))
print ("description: %s" % (mydesc))

# CALLBACK FOR DISCOVERY REQUESTS
def cb_discovery(source, type, size, text):
  print ("%s sent a broadcast!" % (str(source)))
  for d in mydesc:
    s.sendto(discovery.MakePacket(d[0], d[1]), source)
discovery.SetCallback([0], cb_discovery)

# CALLBACK FOR SETTING REQUEST
def cb_setting(source, type, size, text):
  if size > 0:
    try:
      print ("%s is setting my info to %s" % (str(source), text))
      mydesc[0] = (int(text[0]), str(text[1:].decode()))
      WriteIdentity()
    except Exception as e:
      print (e)

discovery.SetCallback([1], cb_setting)

socks = discovery.OpenHostingSockets()

while 1:
  try:
    ready_sockets,outputready,exceptready = select.select(socks,[],[], 1.0)
    for s in ready_sockets:
      message, address = s.recvfrom(100)
      discovery.OnInput(message, address)

    num_hosts = len(discovery.HOSTS)
    discovery.find_hosts()
    if len(discovery.HOSTS) != num_hosts:
      try: s.close()
      except: pass
      finally: socks = discovery.OpenHostingSockets()
  except:
    traceback.print_exc()
    time.sleep(2)
