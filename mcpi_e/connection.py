import socket
import select
import sys
import time
from .util import flatten_parameters_to_bytestring
from .logger import *
import mcpi_e.settings as settings

""" @author: Aron Nieminen, Mojang AB"""

class RequestError(Exception):
    pass

class Connection:
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.lastSent = ""

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            e =  "Drained Data: <%s>\n"%data.strip()
            e += "Last Message: <%s>\n"%self.lastSent.strip()
            sys.stderr.write(e)

    def send(self, f, *data):
        """
        Sends data. Note that a trailing newline '\n' is added here

        The protocol uses CP437 encoding - https://en.wikipedia.org/wiki/Code_page_437
        which is mildly distressing as it can't encode all of Unicode.
        """
        debug("function called:"+f.decode("utf-8") ,data)
   
        if(f==b"world.setBlock"):
             if( abs(data[0][1])>256):
                warn("max height of building is 256")
                return           
        
        #verify setblocks
        if(f==b"world.setBlocks"):
            debug(len(data))
            debug(len(data[0]))
            debug("setblock arg x={} y={} z={} x1={} y1={} z1={} ".format(data[0][0],data[0][1],data[0][2],data[0][3],data[0][4],data[0][5]))
            if(len(data)<1 or len(data[0])<6):
                warn("setBlocks need a6 input parameters setBlocks(x0,y0,z0,x1,y1,z1,blockId)")
                return
         
            
            if( abs(data[0][1])>256 or abs(data[0][4])>256):
                warn("max height of building is 256")
                return
            h=abs(data[0][1]-data[0][4])
            w=abs(data[0][0]-data[0][3])
            l=abs(data[0][2]-data[0][5])
            length=h+w+l
            blocksCount=h*w*l
            debug("set blocks size: h:{}, w:{},l:{}, sum of HWL: {}, total blocks: {} ".format(h,w,l,length,blocksCount))
         
            if(length>300 and blocksCount>1000):
                warn("setBlocks failed, Please limit your block size (h+l+w)<300 and h*l*w<1000. (length:{},blocksize:{})".format(str(length),str(blocksCount)))
                return
      
            
            #print("methods {} not allowed!".format(f.decode("utf-8")))
            #return
      
        s = b"".join([f, b"(", flatten_parameters_to_bytestring(data), b")", b"\n"])
        self._send(s)     
        

    def _send(self, s):
        """
        The actual socket interaction from self.send, extracted for easier mocking
        and testing
        """
        time.sleep(settings.SYS_SPEED) #slow down the running speed
        print("sysspeed:",settings.SYS_SPEED)
        self.drain()
        self.lastSent = s

        self.socket.sendall(s)

    def receive(self):
        """Receives data. Note that the trailing newline '\n' is trimmed"""
        s = self.socket.makefile("r").readline().rstrip("\n")
        if s == Connection.RequestFailed:
            raise RequestError("%s failed"%self.lastSent.strip())
        return s

    def sendReceive(self, *data):
        """Sends and receive data"""
        self.send(*data)
        return self.receive()
    
 
