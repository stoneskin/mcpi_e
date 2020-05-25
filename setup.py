from setuptools import setup

__project__ = 'mcpi_e'
__desc__ = '[for python education] Python library for the Minecraft Pi edition and RaspberryJuice API Modified version'
__version__ = '0.3.0'
__author__ = "stoneskin"
__author_email__ = 'stoneskin@hotmail.com'
__license__ = 'MIT'
__url__ = 'https://github.com/stoneskin/mcpi-e'
#__download_url__="https://github.com/stoneskin/mcpi-e/archive/0.3.0.tar.gz"
__long_description__ = """# Minecraft: Pi edition API Python Library
This project `mcpi-e` is a fork from mcpi project [https://github.com/martinohanlon/mcpi]
`mcpi-e` Python library for communicating with [Minecraft: Pi edition](https://minecraft.net/en-us/edition/pi/) and [RaspberryJuice](https://github.com/zhuowei/RaspberryJuice).

Visit [github.com/stoneskin/mcpi-e](https://github.com/stoneskin/mcpi-e) for more information.
## Installation

### Windows

```
pip3 install --upgrade mcpi-e
```

*Note: you could use `py` or `python -m` to speify the python in your system*

```
py -m pip install --upgrade mcpi-e
```

### Linux / MacOS

```bash
sudo pip3 install --upgrade mcpi-e
```

## Usage

```
from mcpi_e.minecraft import Minecraft
...
mc = Minecraft.create(servername,4711,playerName)

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

"""

__classifiers__ = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Intended Audience :: Developers",
    "Topic :: Education",
    "Topic :: Games/Entertainment",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

setup(name=__project__,
      version = __version__,
      description = __desc__,
      long_description=__long_description__,
      long_description_content_type='text/markdown',
      url = __url__,
      #download_url = __download_url__,
      author = __author__,
      author_email = __author_email__,
      license = __license__,
      packages = [__project__],
      classifiers = __classifiers__,
      zip_safe=False)