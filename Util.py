import libtcodpy as Libtcod
import Event

class ViewPort():
    X = 0
    Y = 0
    
    def __init__(self, width, height):
        self.Width = width
        self.Height = height

class Tile():
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Content = []

class Container():
    Content = []
    Limited = False
    def __init__(self, size):
        self.Size = size

def Clamp(val, low, high):
    return max(low, min(high, val))

class Level():
    def __init__(self, width, height, pathimage):
        self.Map = []
        self.FOVMap = Libtcod.map_new(width, height)
        self.PathImage = pathimage
        Libtcod.map_clear(self.FOVMap, transparent = True, walkable = True)
        self.Width = width
        self.Height = height
        c = -1
        for y in range(height):
            self.Map.append([])
            for x in range(width):
                Global.Tiles.append(Tile())
                c += 1
                Global.Tiles[c].X = x
                Global.Tiles[c].Y = y
                self.Map[y].append(Global.Tiles[c])
                if Libtcod.image_get_pixel(self.PathImage, x, y) == Libtcod.white:
                    Libtcod.map_set_properties(self.FOVMap, x, y, True, False)
    
    Name = "unknown"
    Description = "unknown"
    Level = 0
    Entities = []
    Items = []
    # This will hold any Tile objects that have changed:
    Changes = []

class Body():
    Human = {'head': None, 'body': None, 'hands': None, 'legs': None, 'feet': None}

class Console():
    def __init__(self):
        self.Root = None
        self.GUI = Libtcod.console_new(80, 40)

class Global():
    Tiles = []
    Entities = []
    Items = []
    Events = []