import libtcodpy as Libtcod

def MoveEntity(entity, x, y):
    entity.Move(x, y)

def MoveEntityPath(entity):
    if entity.Path:
        x, y = Libtcod.path_walk(entity.Path, True)
        if not x is None:
            entity.Move(x - entity.X, y - entity.Y)

def Add(event, events):
    if len(events) == 0:
        # If events empty just add event:
        events.append(event)
        return True
    else:
        if event.Unique:
            for e in events:
                if e.Name == event.Name:
                    e.Life += 1
                    return True
        else:
            # Add event seperately:
            events.append(event)
            return True
    
    # If still here then couldn't add:
    return False