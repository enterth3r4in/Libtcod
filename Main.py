from System import *

# Setup mouse and keyboard:
key = Libtcod.Key()
mouse = Libtcod.Mouse()

# Setup test level:
pathimage = Libtcod.image_load("./images/island_block.bmp")
level = Level(80, 40, pathimage)

# Create pointer GUI element for mouse:
guiPointer = GuiChar()
guiPointer.Background = Libtcod.white
guiPointer.Color = Libtcod.white
guiPointer.Blend = Libtcod.BKGND_LIGHTEN
guiPointer.Character = '+'
guiPointer.AddToLevel(level, 0, 0)
Libtcod.mouse_show_cursor(True)

# Create player object:
player = Player()
player.Blend = Libtcod.BKGND_MULTIPLY
player.AddToLevel(level, 40, 15)

ConsoleGUI = Libtcod.console_new(20, 10)
Libtcod.sys_set_fps(30)
Libtcod.console_set_custom_font('./fonts/consolas12.png', Libtcod.FONT_TYPE_GREYSCALE | Libtcod.FONT_LAYOUT_TCOD)
image = Libtcod.image_load("./images/beach.bmp")
#palm = Libtcod.image_load("./images/palm.png")

console = Console()
console.Root = Libtcod.console_init_root(80, 40, 'Game Engine', False)

while not Libtcod.console_is_window_closed():
    Libtcod.sys_check_for_event(Libtcod.EVENT_ANY, key, mouse)
    
    # Handle entity events:
    for tEntity in Global.Entities:
        for tEvent in tEntity.Events:
            tEvent.Run()
            if tEvent.Finished:
                tEntity.Events.remove(tEvent)

    Libtcod.console_clear(console.Root)
    Libtcod.console_clear(console.GUI)
    Libtcod.console_clear(ConsoleGUI)
    #Libtcod.image_blit_2x(image, console.Root, 0, 0, sx=0, sy=0, w=-1, h=-1)
    #Libtcod.image_blit_2x(palm, console.Root, 40, 20, sx=0, sy=0, w=-1, h=-1)
    Libtcod.image_blit_rect(image, console.Root, 0, 0, 80, 40, Libtcod.BKGND_ADD)
    
    Libtcod.console_print(ConsoleGUI, 1, 1, str("FPS: " + str(Libtcod.sys_get_fps())))
    Libtcod.console_print(ConsoleGUI, 1, 2, str(player.X) + ", " + str(player.Y))
    if player.Events:
        Libtcod.console_print(ConsoleGUI, 1, 3, str(player.Events[0].Name))
    Libtcod.console_print(ConsoleGUI, 1, 4, str(image))
    
    # Get the mouse status before checking:
    Libtcod.mouse_get_status()
    
    if mouse.lbutton_pressed:
        player.MoveSpeed = 0.5
        player.Events = []
        player.FindPath(mouse.cx, mouse.cy)
    
    if mouse.rbutton_pressed:
        player.MoveSpeed = 0.05
        player.Events = []
        player.FindPath(mouse.cx, mouse.cy)
    
    if player.Path:
        player.WalkPath()
    
    # Draw mouse pointer:
    guiPointer.SetPosition(mouse.cx, mouse.cy)
    guiPointer.Draw(console.GUI)
    
    for ent in Global.Entities:
        ent.Draw(console.Root)
    #Libtcod.console_blit(Console, 0, 0, level.Width, level.Height, 0, 0, 0)
 
    #handle keys and exit game if needed
    exit = player.HandleKeys()
    if exit:
        break
    
    # Blit GUI elements:
    #Libtcod.image_blit_rect(pathimage, console.Root, 0, 0, -1, -1, Libtcod.BKGND_DARKEN)
    Libtcod.console_blit(ConsoleGUI,0,0,0,0,console.Root,1,1,0.8,0.5)
    Libtcod.console_blit(console.GUI,0,0,0,0,console.Root,0,0,1,0.0)
    
    # Always last:
    Libtcod.console_flush()

