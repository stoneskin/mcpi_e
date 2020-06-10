from mcpi_e.minecraft import Minecraft
from mcpi_e import block
from time import sleep
from random import *

address="192.168.1.155"#if not pass address, it will be localhost
port=4711 #default port for RaspberryJuice plugin
name="stoneskin"
#mc = Minecraft.create()
mc=Minecraft.create(address,port,name)

(x,y,z)=mc.player.getTilePos()

#max height building is 256
#mc.setBlocks(x+1,257,z+1,x+2,y+2+z+2,block.GLASS_PANE.id)


#will return setBlocks failed, Please limit your block size (h+l+w)<300 and h*l*w<1000. (length:311,blocksize:43600)

#mc.setBlocks(x+1,0,z,x+110,200,z+2,0)

#works
mc.setBlocks(x+1,y,z+1,x+2,y,z+2,107)


#mc.setBlock(x+1,y+1,z+1,2)
