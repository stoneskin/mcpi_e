from mcpi_e.rconnection import Rconnection
from .connection import Connection
from .vec3 import Vec3
from .event import BlockEvent, ChatEvent, ProjectileEvent
from .entity import Entity
from .block import Block
import math
from .util import flatten
import sys
from .logger import *
import mcpi_e.settings as settings

""" Minecraft PI low level api v0.1_1

    Note: many methods have the parameter *arg. This solution makes it
    simple to allow different types, and variable number of arguments.
    The actual magic is a mix of flatten_parameters() and __iter__. Example:
    A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

    (Because of this, it's possible to "erase" arguments. CmdPlayer removes
     entityId, by injecting [] that flattens to nothing)

    @author: Aron Nieminen, Mojang AB"""

""" Updated to include functionality provided by RaspberryJuice:
- getBlocks()
- getDirection()
- getPitch()
- getRotation()
- getPlayerEntityId()
- pollChatPosts()
- setSign()
- spawnEntity()
- getEntities()
- removeEntity()
- removeEntityType()
"""


def intFloor(*args):
    return [int(math.floor(x)) for x in flatten(args)]


class CmdPositioner:
    """Methods for setting and getting positions"""

    def __init__(self, connection, packagePrefix):
        self.conn = connection
        self.pkg = packagePrefix

    def getPos(self, id):
        """Get entity position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getPos", id)
        return Vec3(*list(map(float, s.split(","))))

    def setPos(self, id, *args):
        """Set entity position (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setPos", id, args)

    def getTilePos(self, id):
        """Get entity tile position (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getTile", id)
        return Vec3(*list(map(int, s.split(","))))

    def setTilePos(self, id, *args):
        """Set entity tile position (entityId:int) => Vec3"""
        self.conn.send(self.pkg + b".setTile", id, intFloor(*args))

    def setDirection(self, id, *args):
        """Set entity direction (entityId:int, x,y,z)"""
        self.conn.send(self.pkg + b".setDirection", id, args)

    def getDirection(self, id):
        """Get entity direction (entityId:int) => Vec3"""
        s = self.conn.sendReceive(self.pkg + b".getDirection", id)
        return Vec3(*map(float, s.split(",")))

    def setRotation(self, id, yaw):
        """Set entity rotation (entityId:int, yaw)"""
        self.conn.send(self.pkg + b".setRotation", id, yaw)

    def getRotation(self, id):
        """get entity rotation (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getRotation", id))

    def setPitch(self, id, pitch):
        """Set entity pitch (entityId:int, pitch)"""
        self.conn.send(self.pkg + b".setPitch", id, pitch)

    def getPitch(self, id):
        """get entity pitch (entityId:int) => float"""
        return float(self.conn.sendReceive(self.pkg + b".getPitch", id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + b".setting", setting, 1 if bool(status) else 0)


class CmdEntity(CmdPositioner):
    """Methods for entities"""

    def __init__(self, connection):
        CmdPositioner.__init__(self, connection, b"entity")

    def getName(self, id):
        """Get the list name of the player with entity id => [name:str]
        
        Also can be used to find name of entity if entity is not a player."""
        return self.conn.sendReceive(b"entity.getName", id)

    def getEntities(self, id, distance=10, typeId=-1):
        """Return a list of entities near entity (playerEntityId:int, distanceFromPlayerInBlocks:int, typeId:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        s = self.conn.sendReceive(b"entity.getEntities", id, distance, typeId)
        entities = [e for e in s.split("|") if e]
        return [[int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]),
                 float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]

    def removeEntities(self, id, distance=10, typeId=-1):
        """Remove entities all entities near entity (playerEntityId:int, distanceFromPlayerInBlocks:int, typeId:int, ) => (removedEntitiesCount:int)"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        return int(self.conn.sendReceive(b"entity.removeEntities", id, distance, typeId))

    def pollBlockHits(self, *args):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"entity.events.block.hits", intFloor(args))
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self, *args):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"entity.events.chat.posts", intFloor(args))
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

    def pollProjectileHits(self, *args):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"entity.events.projectile.hits", intFloor(args))
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]),
                int(info[1]),
                int(info[2]),
                int(info[3]),
                info[4],
                info[5]))
        return results

    def clearEvents(self, *args):
        """Clear the entities events"""
        self.conn.send(b"entity.events.clear", intFloor(args))


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""

    def __init__(self, connection, playerId):
        CmdPositioner.__init__(self, connection, b"player")
        self.conn = connection
        self.playerId = playerId

    def getPos(self):
        return CmdPositioner.getPos(self, self.playerId)

    def setPos(self, *args):
        return CmdPositioner.setPos(self, self.playerId, args)

    def getTilePos(self):
        return CmdPositioner.getTilePos(self, self.playerId)

    def setTilePos(self, *args):
        return CmdPositioner.setTilePos(self, self.playerId, args)

    def setDirection(self, *args):
        return CmdPositioner.setDirection(self, self.playerId, args)

    def getDirection(self):
        return CmdPositioner.getDirection(self, self.playerId)

    def setRotation(self, yaw):
        return CmdPositioner.setRotation(self, self.playerId, yaw)

    def getRotation(self):
        return CmdPositioner.getRotation(self, self.playerId)

    def setPitch(self, pitch):
        return CmdPositioner.setPitch(self, self.playerId, pitch)

    def getPitch(self):
        return CmdPositioner.getPitch(self, self.playerId)

    def getEntities(self, distance=10, typeId=-1):
        """Return a list of entities near entity (distanceFromPlayerInBlocks:int, typeId:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        s = self.conn.sendReceive(b"player.getEntities", distance, typeId)
        entities = [e for e in s.split("|") if e]
        return [[int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]),
                 float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]

    def removeEntities(self, distance=10, typeId=-1):
        """Remove entities all entities near entity (distanceFromPlayerInBlocks:int, typeId:int, ) => (removedEntitiesCount:int)"""
        """If distanceFromPlayerInBlocks:int is not specified then default 10 blocks will be used"""
        return int(self.conn.sendReceive(b"player.removeEntities", distance, typeId))

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"player.events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"player.events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

    def pollProjectileHits(self):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"player.events.projectile.hits")
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]),
                int(info[1]),
                int(info[2]),
                int(info[3]),
                info[4],
                info[5]))
        return results

    def clearEvents(self):
        """Clear the players events"""
        self.conn.send(b"player.events.clear")


class CmdPlayerEntity(CmdPlayer):
    """ use entity to build a player """

    def __init__(self, connection, playerId):
        CmdPositioner.__init__(self, connection, b"entity")
        self.conn = connection
        self.playerId = playerId

    def getPos(self):
        return CmdPositioner.getPos(self, self.playerId)


class CmdCamera:
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entityId])"""
        self.conn.send(b"camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view"""
        self.conn.send(b"camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entityId])"""
        self.conn.send(b"camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send(b"camera.setPos", args)


class CmdEvents:
    """Events"""

    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events"""
        self.conn.send(b"events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.block.hits")
        events = [e for e in s.split("|") if e]
        return [BlockEvent.Hit(*list(map(int, e.split(",")))) for e in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        s = self.conn.sendReceive(b"events.chat.posts")
        events = [e for e in s.split("|") if e]
        return [ChatEvent.Post(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in events]

    def pollProjectileHits(self):
        """Only triggered by projectiles => [BlockEvent]"""
        s = self.conn.sendReceive(b"events.projectile.hits")
        events = [e for e in s.split("|") if e]
        results = []
        for e in events:
            info = e.split(",")
            results.append(ProjectileEvent.Hit(
                int(info[0]),
                int(info[1]),
                int(info[2]),
                int(info[3]),
                info[4],
                info[5]))
        return results


class Minecraft:
    """The main class to interact with a running instance of Minecraft Pi."""

    def __init__(self, raspberryConnection, rconConnection, playerId, playerName):
        self.conn = raspberryConnection
        self.rconn = rconConnection

        self.camera = CmdCamera(raspberryConnection)
        self.entity = CmdEntity(raspberryConnection)
        self.cmdplayer = CmdPlayer(raspberryConnection, playerId)
        self.player = CmdPlayerEntity(raspberryConnection, playerId)
        self.events = CmdEvents(raspberryConnection)
        self.playerName = playerName
        self.settings = settings

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.sendReceive(b"world.getBlock", intFloor(args)))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block"""
        ans = self.conn.sendReceive(b"world.getBlockWithData", intFloor(args))
        return Block(*list(map(int, ans.split(","))))

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        s = self.conn.sendReceive(b"world.getBlocks", intFloor(args))
        return map(int, s.split(","))

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        if len(args) > 4:
            self.conn.send(b"world.setBlocks",
                           intFloor(args[0], args[1], args[2], args[0], args[1], args[2], args[3], args[4]))
        else:
            self.conn.send(b"world.setBlock", intFloor(args))

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0,y0,z0,x1,y1,z1,id,[data])"""
        self.conn.send(b"world.setBlocks", intFloor(args))

    def setSign(self, *args):
        """Set a sign (x,y,z,id,data,[line1,line2,line3,line4])
        
        Wall signs (id=68) require data for facing direction 2=north, 3=south, 4=west, 5=east
        Standing signs (id=63) require data for facing rotation (0-15) 0=south, 4=west, 8=north, 12=east
        @author: Tim Cummings https://www.triptera.com.au/wordpress/"""
        lines = []
        flatargs = []
        for arg in flatten(args):
            flatargs.append(arg)
        for flatarg in flatargs[5:]:
            lines.append(flatarg.replace(",", ";").replace(")", "]").replace("(", "["))
        self.conn.send(b"world.setSign", intFloor(flatargs[0:5]) + lines)

    def spawnEntity(self, *args):
        """Spawn entity (x,y,z,id)"""
        return int(self.conn.sendReceive(b"world.spawnEntity", args))

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.sendReceive(b"world.getHeight", intFloor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.sendReceive(b"world.getPlayerIds")
        return list(map(int, ids.split("|")))

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return int(self.conn.sendReceive(b"world.getPlayerId", name))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send(b"world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send(b"world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.conn.send(b"chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.conn.send(b"world.setting", setting, 1 if bool(status) else 0)

    def getEntityTypes(self):
        """Return a list of Entity objects representing all the entity types in Minecraft"""
        s = self.conn.sendReceive(b"world.getEntityTypes")
        types = [t for t in s.split("|") if t]
        return [Entity(int(e[:e.find(",")]), e[e.find(",") + 1:]) for e in types]

    def getEntities(self, typeId=-1):
        """Return a list of all currently loaded entities (EntityType:int) => [[entityId:int,entityTypeId:int,entityTypeName:str,posX:float,posY:float,posZ:float]]"""
        s = self.conn.sendReceive(b"world.getEntities", typeId)
        entities = [e for e in s.split("|") if e]
        return [[int(n.split(",")[0]), int(n.split(",")[1]), n.split(",")[2], float(n.split(",")[3]),
                 float(n.split(",")[4]), float(n.split(",")[5])] for n in entities]

    def removeEntity(self, id):
        """Remove entity by id (entityId:int) => (removedEntitiesCount:int)"""
        return int(self.conn.sendReceive(b"world.removeEntity", int(id)))

    def removeEntities(self, typeId=-1):
        """Remove entities all currently loaded Entities by type (typeId:int) => (removedEntitiesCount:int)"""
        return int(self.conn.sendReceive(b"world.removeEntities", typeId))

    ### + DRAWING ADDITIONAL COMMANDS ###
    # draw point
    def drawPoint3d(self, x, y, z, blockType, blockData=0):
        self.setBlock(x, y, z, blockType, blockData)
        # print "x = " + str(x) + ", y = " + str(y) + ", z = " + str(z)

    # draws a face, when passed a collection of vertices which make up a polyhedron
    def drawFace(self, vertices, filled, blockType, blockData=0):
        # get the edges of the face
        edgesVertices = []
        # persist first vertex
        firstVertex = vertices[0]
        # get last vertex
        lastVertex = vertices[0]
        # loop through vertices and get edges
        for vertex in vertices[1:]:
            # got 2 vertices, get the points for the edge
            edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y,
                                                         vertex.z)
            # persist the last vertex found
            lastVertex = vertex
        # get edge between the last and first vertices
        edgesVertices = edgesVertices + self.getLine(lastVertex.x, lastVertex.y, lastVertex.z, firstVertex.x,
                                                     firstVertex.y, firstVertex.z)

        if (filled):
            # draw solid face
            # sort edges vertices
            def keyX(point):
                return point.x

            def keyY(point):
                return point.y

            def keyZ(point):
                return point.z

            edgesVertices.sort(key=keyZ)
            edgesVertices.sort(key=keyY)
            edgesVertices.sort(key=keyX)

            # draw lines between the points on the edges
            # this algorithm isnt very efficient, but it does always fill the gap
            lastVertex = edgesVertices[0]
            for vertex in edgesVertices[1:]:
                # got 2 vertices, draw lines between them
                self.drawLine(lastVertex.x, lastVertex.y, lastVertex.z, vertex.x, vertex.y, vertex.z, blockType,
                              blockData)
                # print "x = " + str(lastVertex.x) + ", y = " + str(lastVertex.y) + ", z = " + str(lastVertex.z) + " x2 = " + str(vertex.x) + ", y2 = " + str(vertex.y) + ", z2 = " + str(vertex.z)
                # persist the last vertex found
                lastVertex = vertex

        else:
            # draw wireframe
            self.drawVertices(edgesVertices, blockType, blockData)

    # draw's all the points in a collection of vertices with a block
    def drawVertices(self, vertices, blockType, blockData=0):
        for vertex in vertices:
            self.drawPoint3d(vertex.x, vertex.y, vertex.z, blockType, blockData)

    # draw line
    def drawLine(self, x1, y1, z1, x2, y2, z2, blockType, blockData=0):
        self.drawVertices(self.getLine(x1, y1, z1, x2, y2, z2), blockType, blockData)

    # draw sphere
    def drawSphere(self, x1, y1, z1, radius, blockType, blockData=0):
        # create sphere
        for x in range(radius * -1, radius):
            for y in range(radius * -1, radius):
                for z in range(radius * -1, radius):
                    if x ** 2 + y ** 2 + z ** 2 < radius ** 2:
                        self.drawPoint3d(x1 + x, y1 + y, z1 + z, blockType, blockData)

    # draw a verticle circle
    def drawCircle(self, x0, y0, z, radius, blockType, blockData=0):
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius
        self.drawPoint3d(x0, y0 + radius, z, blockType, blockData)
        self.drawPoint3d(x0, y0 - radius, z, blockType, blockData)
        self.drawPoint3d(x0 + radius, y0, z, blockType, blockData)
        self.drawPoint3d(x0 - radius, y0, z, blockType, blockData)

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            self.drawPoint3d(x0 + x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 + y, z, blockType, blockData)
            self.drawPoint3d(x0 + x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 - x, y0 - y, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 + x, z, blockType, blockData)
            self.drawPoint3d(x0 + y, y0 - x, z, blockType, blockData)
            self.drawPoint3d(x0 - y, y0 - x, z, blockType, blockData)

    # draw a horizontal circle
    def drawHorizontalCircle(self, x0, y, z0, radius, blockType, blockData=0):
        f = 1 - radius
        ddf_x = 1
        ddf_z = -2 * radius
        x = 0
        z = radius
        self.drawPoint3d(x0, y, z0 + radius, blockType, blockData)
        self.drawPoint3d(x0, y, z0 - radius, blockType, blockData)
        self.drawPoint3d(x0 + radius, y, z0, blockType, blockData)
        self.drawPoint3d(x0 - radius, y, z0, blockType, blockData)

        while x < z:
            if f >= 0:
                z -= 1
                ddf_z += 2
                f += ddf_z
            x += 1
            ddf_x += 2
            f += ddf_x
            self.drawPoint3d(x0 + x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 + z, blockType, blockData)
            self.drawPoint3d(x0 + x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 - x, y, z0 - z, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 + x, blockType, blockData)
            self.drawPoint3d(x0 + z, y, z0 - x, blockType, blockData)
            self.drawPoint3d(x0 - z, y, z0 - x, blockType, blockData)

    # returns points on a line
    # 3d implementation of bresenham line algorithm
    def getLine(self, x1, y1, z1, x2, y2, z2):

        # return maximum of 2 values
        def MAX(a, b):
            if a > b:
                return a
            else:
                return b

        # return step
        def ZSGN(a):
            if a < 0:
                return -1
            elif a > 0:
                return 1
            elif a == 0:
                return 0

        # list for vertices
        vertices = []

        # if the 2 points are the same, return single vertice
        if (x1 == x2 and y1 == y2 and z1 == z2):
            vertices.append(Vec3(x1, y1, z1))

        # else get all points in edge
        else:

            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1

            ax = abs(dx) << 1
            ay = abs(dy) << 1
            az = abs(dz) << 1

            sx = ZSGN(dx)
            sy = ZSGN(dy)
            sz = ZSGN(dz)

            x = x1
            y = y1
            z = z1

            # x dominant
            if (ax >= MAX(ay, az)):
                yd = ay - (ax >> 1)
                zd = az - (ax >> 1)
                loop = True
                while (loop):
                    vertices.append(Vec3(x, y, z))
                    if (x == x2):
                        loop = False
                    if (yd >= 0):
                        y += sy
                        yd -= ax
                    if (zd >= 0):
                        z += sz
                        zd -= ax
                    x += sx
                    yd += ay
                    zd += az
            # y dominant
            elif (ay >= MAX(ax, az)):
                xd = ax - (ay >> 1)
                zd = az - (ay >> 1)
                loop = True
                while (loop):
                    vertices.append(Vec3(x, y, z))
                    if (y == y2):
                        loop = False
                    if (xd >= 0):
                        x += sx
                        xd -= ay
                    if (zd >= 0):
                        z += sz
                        zd -= ay
                    y += sy
                    xd += ax
                    zd += az
            # z dominant
            elif (az >= MAX(ax, ay)):
                xd = ax - (az >> 1)
                yd = ay - (az >> 1)
                loop = True
                while (loop):
                    vertices.append(Vec3(x, y, z))
                    if (z == z2):
                        loop = False
                    if (xd >= 0):
                        x += sx
                        xd -= az
                    if (yd >= 0):
                        y += sy
                        yd -= az
                    z += sz
                    xd += ax
                    yd += ay

        return vertices

    ### - DRAWING ADDITIONAL COMMANDS ###

    ### + RCON ADDITIONAL COMMANDS ###
    def summonCreature(self, x, y, z, creature, data=""):
        return self.rconn.sendReceive(f"/summon {creature} ~{x} ~{y} ~{z} {data}")

    def setTime(self, daytime):
        return self.rconn.sendReceive(f"/time set {daytime}")

    def stopTime(self, isStopped):
        if isStopped:
            return self.rconn.sendReceive(f"/gamerule doDaylightCycle false")
        else:
            return self.rconn.sendReceive(f"/gamerule doDaylightCycle true")

    def setWeather(self, weather, duration=60 * 5):
        return self.rconn.sendReceive(f"/weather {weather} {duration}")

    # survival/creative/adventure(0/1/2)
    def setGamemode(self, whom, gamemode):
        return self.rconn.sendReceive(f"/gamemode {gamemode} {whom}")

    # peaceful/easy/normal/hard (0,1,2,3)
    def setDifficulty(self, difficulty):
        return self.rconn.sendReceive(f"/difficulty {difficulty}")

    def giveItem(self, whom, item, count=1):
        return self.rconn.sendReceive(f"/give {whom} {item} {count}")

    def giveItemToMe(self, item, count=1):
        return self.rconn.sendReceive(f"/give {self.playerName} {item} {count}")

    def teleport(self, x, y, z):
        return self.rconn.sendReceive(f"/tp {self.playerName} {x} {y} {z}")

    def teleportToMe(self, whom):
        return self.rconn.sendReceive(f"/tp {whom} {self.playerName}")

    def setWorldspawn(self, x, y, z):
        return self.rconn.sendReceive(f"/setworldspawn {x} {y} {z}")

    def clearInventory(self, person):
        return self.rconn.sendReceive(f"/clear {person}")

    def cloneBlocks(self, x1, y1, z1, x2, y2, z2, x, y, z):
        return self.rconn.sendReceive(f"/clone {x1} {y1} {z1} {x2} {y2} {z2} {x} {y} {z}")

    def setEffect(self, whom, effect, duration=20, power=10):
        return self.rconn.sendReceive(f"/effect {whom} {effect} {duration} {power}")

    def setEntityData(self, whom, data):
        return self.rconn.sendReceive(f"/entitydata {whom} {data}")

    ### - RCON ADDITIONAL COMMANDS ###

    @staticmethod
    def create(address="localhost", rasberryPort=4711, rconPort=8711, rconPassword=47118711, playerName=""):
        log("Running Python version:" + sys.version)
        conn = Connection(address, rasberryPort)
        rconn = Rconnection(address, rconPort, rconPassword)
        playerId = []
        if playerName != "":
            playerId = int(conn.sendReceive(b"world.getPlayerId", playerName))
            log("get {} playerid={}".format(playerName, playerId))

        return Minecraft(conn, rconn, playerId, playerName)


# settings
if __name__ == "__main__":
    # initSettings()
    mc = Minecraft.create()
    mc.postToChat("Hello, Minecraft!")
