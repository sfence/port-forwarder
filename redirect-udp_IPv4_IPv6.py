
import socket;
import select;
import threading;
import time;

bufsize = 1024 

# set these values
target_host = "2a01:4240:6441:8928::1"
target_port = 30000

listen_host = ""
listen_port = 30000

clients_dict = dict();

class RedirectTargetSource(threading.Thread):
  def __init__(self, config):
    threading.thread.__init__(self)
    self.target_socket = config['redirect_socket']
    self.source_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.source_addr = config['source_addr']
    print("*** Listening IPv6 for {}:{}".format( self.source_addr[0], self.source_addr[1] ))
    self.lifetime = time.time()+5.0;
    self.nowtime = self.lifetime;
  
  def run(self):
    while self.lifetime>=self.nowtime:
      try:
        data, addr = self.target_socket.recvfrom();
        if data:
          self.source_socket.sendto(data, self.source_addr);
        self.lifetime = time.time()+5.0;
      except:
        # ignore exception
        pass;
      self.nowtime = time.time();
    
    del socket_target_source[self.source_addr]
    self.target_socket.close();
    self.source_socket.close();

def listen(host, port):
  listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  listen_socket.bind((host, port))
  print("*** Listening IPv4 on {}:{}".format( host, port ))
  while True:
    data, addr = listen_socket.recvfrom(bufsize)
    if addr not in socket_target_source:
      target_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM);
      clients_dict[addr] = dict(target_socket=target_socket, source_addr=addr);
      thread = RedirectTargetSource(clients_dict[addr])
      thread.start();
    else:
      target_socket = clients_dict[addr][target_socket];
    if data:
      print("*** Redirecting: '{}' from port {}".format(data, addr[1]));
      target_socket.sendto(data, (target_host, target_port));

listen(listen_host, listen_port)

