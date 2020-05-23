# [For Python Education] Minecraft: Pi edition API Python Library modified version

This project `mcpi-e` is a fork from `mcpi` project [https://github.com/martinohanlon/mcpi]
`mcpi` Python library for communicating with [Minecraft: Pi edition](https://minecraft.net/en-us/edition/pi/) and [RaspberryJuice](https://github.com/zhuowei/RaspberryJuice).

I make some change for my students to use in the class lab. 

## Installation

### Windows

```
pip3 install mcpi-e
```

*Note: you could use `py` or `python -m` to speify the python in your system*

```
py -m pip install mcpi-e
```

### Linux / MacOS

```bash
sudo pip3 install mcpi-e
```

## `mcpi-e` Change log

### 1. Enhancement for using `mcpi` in server with multiple users

- User could pass player username as 3rd parameter when create a new Minecraft api instense.
  
   ex:
   `mc=Minecraft.create(address,port,name)`

- Change mc.Player to use entity so it will not pick the first user in the server.

### 2. Limit the Usage of `mcpi`  

- Add the _send command 0.05s interval to slow down the speed
- limit the useage of setBlocks 
- todo: limit the script usage range (x,y,z)

## History

The [Minecraft: Pi edition](https://minecraft.net/en-us/edition/pi/) Python library was originally created by Mojang and released with Minecraft: Pi edition.

Initial supported was provided for Python 2 only, but during a sprint at PyconUK 2014 it was migrated to Python 3 and [py3minepi](https://github.com/py3minepi/py3minepi) was created.

The ability to hack Minecraft from Python was very popular and the [RaspberryJuice](https://github.com/zhuowei/RaspberryJuice) plugin was created for Minecraft Java edition. RaspberryJuice also extended the API adding additional features.

This python library supports Python 2 & 3 and Minecraft: Pi edition and RaspberryJuice.

Documentation for the Minecraft: Pi edition and RaspberryJuice API's can be found at [www.stuffaboutcode.com/p/minecraft-api-reference.html](http://www.stuffaboutcode.com/p/minecraft-api-reference.html).

It was released onto [PyPI](https://pypi.org) in May 2018.

If you want some cool additional tools for modifying Minecraft, check out [minecraft-stuff](https://minecraft-stuff.readthedocs.io/en/latest/).

## Sources

This library is a collection of the following sources:

+ [Minecraft: Pi edition](https://minecraft.net/en-us/edition/pi/)
+ [Python 3 Minecraft: Pi edition library](https://github.com/py3minepi/py3minepi)

## Licenses

+ mcpi - [LICENSE.txt](https://github.com/martinohanlon/mcpi/blob/master/LICENSE)
+ Minecraft: Pi edition LICENSE - [minecraft-pi-edition-LICENSE.txt](https://github.com/martinohanlon/mcpi/blob/master/minecraft-pi-edition-LICENSE.txt)

