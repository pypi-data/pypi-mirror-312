import os
from threading import Lock
import socket
import struct
import time
import pickle

current_folder = os.path.dirname(os.path.abspath(__file__))


class CONVERTER:
    def __init__(self) -> None:
        with open(os.path.join(current_folder,"itemNameToId.pkl"), "rb") as file:  # rb: read binary
            self.itemNameToId = pickle.load(file)
        with open(os.path.join(current_folder,"idToItemName.pkl"), "rb") as file:  # rb: read binary
            self.idToItemName = pickle.load(file)

    def getId(self,itemName):
        return self.itemNameToId.get(itemName,None)
    
    def getName(self,id):
        return self.idToItemName.get(id,None)



class DB:
    sell = 0
    buyOrder = 1
    smart = 2

class SITE:
    youpin = 0
    buff163 = 1

class FAST_PRICE():
    def __init__(self,host="103.74.106.225",port=3000,api_key="") -> None:
        self.lock = Lock()
        self.host = host
        self.client_socket = None
        self.port = port
        self.api_key = api_key
        self.conveter = CONVERTER()
        self.__connect()

    def __connect(self):
        while True:
            try:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))
                self.client_socket.sendall(self.api_key.encode())
                print(self.client_socket.recv(1024).decode())
                return
            except:
                time.sleep(10)
        
    def get(self,site:SITE,itemId:int,float:int=255,fate:int=255,db:DB=0):
        with self.lock: 
            while True:
                try:
                    self.client_socket.sendall(struct.pack('<BBHBBBQ', 0,site,itemId,float,fate,db,0))
                    return int.from_bytes(self.client_socket.recv(8), byteorder='little')
                except Exception as e:
                    print(e)
                    time.sleep(10)
                    self.__connect()

    def __del__(self):
        if self.client_socket:
            self.client_socket.close()



# c = FAST_PRICE(api_key="c8f5b40c-3c56-44c2-afa3-3c3eb735e7fc")

# print(c.get(site=SITE.buff163,itemId=c.conveter.getId("AK-47 | Asiimov (Battle-Scarred)"),db=DB.sell,float=255))

