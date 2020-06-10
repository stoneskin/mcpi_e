from mcpi_e.minecraft import Minecraft
from mcpi_e import block
from time import sleep
from random import *


address="192.168.1.155"#if not pass address, it will be localhost
port=4711 #default port for RaspberryJuice plugin 4711
name="stoneskin"
#mc = Minecraft.create()
mc=Minecraft.create(address,port,name)

currentId=0
while(True):
    x,y,z=mc.player.getTilePos()
    id=mc.getBlock(x,y-1,z)
    if(id!=currentId):
        print(str(id))
    currentId=id