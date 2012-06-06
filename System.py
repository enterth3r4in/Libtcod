from Util import *

class Object():
    X = 0
    Y = 0
    Depth = 0
    Tile = 0
    Color = Libtcod.white
    Background = Libtcod.black
    Blend = Libtcod.BKGND_NONE
    Character = "*"
    Solid = False
    Visible = True
    Name = "unknown"
    Type = "object"
    Description ="""unavailable
    """
    Events = []
    
    def Draw(self, console):
        if self.Visible:
            #Libtcod.console_put_char_ex(console, self.X, self.Y, self.Character, self.Color, self.Background)
            Libtcod.console_put_char(console, self.X, self.Y, self.Character, self.Blend)
            Libtcod.console_set_char_foreground(console, self.X, self.Y, self.Color)
            if self.Background:
                Libtcod.console_set_char_background(console, self.X, self.Y, self.Background, self.Blend)
    
    def AddToLevel(self, level, x, y):
        x = Clamp(x, 0, level.Width - 1)
        y = Clamp(y, 0, level.Height - 1)
        self.Level = level
        self.X = x
        self.Y = y
        if level.Map[y][x]:
            level.Map[y][x].Content.append(self)
    
    def SetPosition(self, x, y):
        self.Level.Changes.append(self.Level.Map[self.Y][self.X])
        self.Level.Map[self.Y][self.X].Content.remove(self)
        #Libtcod.map_set_properties(self.Level.FOVMap, x, y, True, True)
        self.X = x
        self.Y = y
        self.X = Clamp(self.X, 0, self.Level.Width - 1)
        self.Y = Clamp(self.Y, 0, self.Level.Height - 1)
        self.Level.Map[self.Y][self.X].Content.append(self)
        #Libtcod.map_set_properties(self.Level.FOVMap, x, y, True, False)

class GuiChar(Object):
    Type = "gui"

class Entity(Object):
    def __init__(self):
        Global.Entities.append(self)
    
    Race = "human"
    Type = "entity"
    Character = "@"
    Level = None
    Health = 10
    Damage = 1
    Inventory = Container(10)
    Equipment = Body.Human
    Path = None
    PathSize = 0
    MoveSpeed = 0.1
    State = "none"
    
    def AddItem(self, item):
        if len(self.Inventory.Content) < self.Inventory.Size:
            self.Inventory.Content.append(item)
            item.Owner = self
    
    def RemoveItem(self, item):
        self.Inventory.Content.remove(item)
    
    def Move(self, x, y):
        self.Level.Changes.append(self.Level.Map[self.Y][self.X])
        self.Level.Map[self.Y][self.X].Content.remove(self)
        self.X += x
        self.Y += y
        self.X = Clamp(self.X, 0, self.Level.Width - 1)
        self.Y = Clamp(self.Y, 0, self.Level.Height - 1)
        self.Level.Map[self.Y][self.X].Content.append(self)
    
    def FindPath(self, x, y):
        if self.Level:
            path = Libtcod.path_new_using_map(self.Level.FOVMap, 1.41)
            Libtcod.path_compute(path, self.X, self.Y, x, y)
            if not Libtcod.path_is_empty(path):
                self.PathSize = Libtcod.path_size(path)
                self.Path = path
                return True
            else:
                self.Path = None
                self.PathSize = 0
                return False
    
    def WalkPath(self):
        if self.Path:
            x, y = Libtcod.path_get_destination(self.Path)
            if x == self.X and y == self.Y:
                Libtcod.path_delete(self.Path)
                self.Path = None
            else:
                event = Event("PlayerMove", self, [self], self.MoveSpeed, True, True, 0, Events.MoveEntityPath, [self])
                Events.Add(event, self.Events)

class Player(Entity):
    Type = "player"
    Description = "This is you."
    
    def HandleKeys(self):
        # movement keys
        # Event(name, owner, target, duration, oneoff, unique, quant, function, params)
        if Libtcod.console_is_key_pressed(Libtcod.KEY_UP):
            #player.Move(0, -1)
            event = Event("PlayerMove", self, [self], self.MoveSpeed, True, True, 0, Events.MoveEntity, [self, 0, -1])
            Events.Add(event, self.Events)
 
        elif Libtcod.console_is_key_pressed(Libtcod.KEY_DOWN):
            event = Event("PlayerMove", self, [self], self.MoveSpeed, True, True, 0, Events.MoveEntity, [self, 0, 1])
            Events.Add(event, self.Events)
 
        elif Libtcod.console_is_key_pressed(Libtcod.KEY_LEFT):
            event = Event("PlayerMove", self, [self], self.MoveSpeed, True, True, 0, Events.MoveEntity, [self, -1, 0])
            Events.Add(event, self.Events)
 
        elif Libtcod.console_is_key_pressed(Libtcod.KEY_RIGHT):
            event = Event("PlayerMove", self, [self], self.MoveSpeed, True, True, 0, Events.MoveEntity, [self, 1, 0])
            Events.Add(event, self.Events)
    
        key = Libtcod.console_check_for_keypress()
        if key.vk == Libtcod.KEY_ENTER and key.lalt:
            #Alt+Enter: toggle fullscreen
            Libtcod.console_set_fullscreen(not Libtcod.console_is_fullscreen())
 
        elif key.vk == Libtcod.KEY_ESCAPE:
            return True  #exit game

class Item(Object):
    def __init__(self):
        Global.Items.append(self)
    Type = "item"
    Character = ","
    Stackable = False
    Contents = False
    Owner = None

class Terrain(Object):
    Type = "terrain"
    Character = "#"
    Indestructible = True
    
    