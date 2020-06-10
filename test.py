from mcpi_e.minecraft import Minecraft
from mcpi_e import block
from time import sleep
from random import *
from mcpi_e.logger import *

address="192.168.1.155"#if not pass address, it will be localhost
port=471 #default port for RaspberryJuice plugin 4711
name="stoneskin"

#mc = Minecraft.create()
mc=Minecraft.create(address,port,name)
debug("debug")
warn("warn")
log("log")

mc.settings.SHOW_DEBUG=False
print("Is show debug msg",mc.settings.SHOW_DEBUG)
print("Is show log msg",mc.settings.SHOW_Log)
print("system speed:",mc.settings.SYS_SPEED)
mc.settings.SYS_SPEED=mc.settings.Speed.FAST
(x,y,z)=pos=mc.player.getTilePos()
debug("this will not dispaly")
log(pos)
warn("warn")


