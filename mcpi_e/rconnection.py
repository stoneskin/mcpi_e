import socket
import select
import sys
import time
from .util import flatten_parameters_to_bytestring
from .logger import *
import mcpi_e.settings as settings
from mcrcon import MCRcon

""" @author: Aron Nieminen, Mojang AB"""


class RequestError(Exception):
    pass


class Rconnection:
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"

    def __init__(self, address, port, password):
        self.rconn = MCRcon(host=address, port=port, password=password)
        self.rconn.connect()
        self.lastSent = ""

    def sendReceive(self, command):
        """
        Sends data by RCON. Note that a trailing newline '\n' is added here

        The protocol uses CP437 encoding - https://en.wikipedia.org/wiki/Code_page_437
        which is mildly distressing as it can't encode all of Unicode.
        """
        print(f"-> sendReceive RCON: {command}")
        # time.sleep(5)
        result = self.rconn.command(command)
        print(f"<- sendReceive RCON: {result}")
        return result
