import libtcodpy as Libtcod

class SubEvent():
    def __init__(self, duration):
        self.Instant = False
        self.Duration = duration
        self.MaxDuration = duration

class Create():
    def __init__(self, name, sdur, mdur, edur, func, params):
        self.Stacked = False
        self.Unique = False
        self.Stack = 1
        # -1 is infinite:
        self.MaxStack = -1
        
        self.Start = SubEvent(sdur)
        if sdur == -1:
            self.Start.Instant = True
        self.Middle = SubEvent(mdur)
        if mdur == -1:
            self.Middle.Instant = True
        self.End = SubEvent(edur)
        if edur == -1:
            self.End.Instant = True

        self.Function = func
        self.Parameters = params
        self.Targets = []
        self.Owner = None
        self.OnEnd = True # This determines whether the middle event runs during or at the end of the duration.
        self.State = "Start"
        self.Id = name
        self.DT = 0
    
    def Run(self):
        self.DT = Libtcod.sys_get_last_frame_length()
        if self.State == "Start":
            if not self.Start.Instant:
                self.Start.Duration -= self.DT
            else:
                self.State = "Middle"
                return True
            if self.Start.Duration <= 0:
                self.State = "Middle"
                self.Middle.Duration += self.Start.Duration
                return True
            return True
        if self.State == "Middle":
            # Needs expanding to run event functions:
            self.Middle.Duration -= Libtcod.sys_get_last_frame_length()
            if self.OnEnd:
                if self.Middle.Duration <= 0:
                    self.Function(self, *self.Parameters)
                    self.State = "End"
                    return True
            else:
                self.DT = Libtcod.sys_get_last_frame_length()
                self.Function(self, *self.Parameters)
                if self.Middle.Duration <= 0:
                    self.State = "End"
                    return True
                    dt = 1
                return True
            return False
        if self.State == "End":
            if not self.End.Instant: # not instant
                self.End.Duration -= self.DT
            else:
                if not self.Unique:
                    if self.Stacked and self.Stack > 0:
                        self.Stack -= 1
                        self.Start.Duration = self.Start.MaxDuration
                        self.Middle.Duration = self.Middle.MaxDuration
                        self.End.Duration = self.End.MaxDuration
                        self.State = "Start"
                        return True
                self.State = "Finished"
                return True
            if self.End.Duration <= 0:
                if not self.Unique:
                    if self.Stacked and self.Stack > 0:
                        self.Stack -= 1
                        self.Start.Duration = self.Start.MaxDuration + self.End.Duration
                        self.Middle.Duration = self.Middle.MaxDuration
                        self.End.Duration = self.End.MaxDuration
                        self.State = "Start"
                        return True
                    else:
                        self.State = "Finished"
                        return True
                self.State = "Finished"
            return True
        else:
            return False

# Start, Middle, End subevents
# Instant or timed (Instant = True or False)
# MaxStack, Stack, Stacked (True = One after the other and False = Added/ran each time / concurrent)
# Unique

def Add(event, elist):
    found = False
    other = None
    try:
        # If the event list is empty we just add:
        if len(elist) == 0:
            elist.append(event)
            return True # Event added.
        else:
            # First see if there is already the same id event in event list:
            for e in elist:
                if e.Id == event.Id:
                    found = True
                    other = e
            # If we find an event:
            if found and other:
                if event.Unique:
                    return False # Cannot add as already added and unique.
                if event.Stacked:
                    if other.MaxStack == -1: # Infinite max stack.
                        other.Stack += 1
                        return True # Event added to other same event stack
                    elif not other.Stack + 1 > other.MaxStack:
                        other.Stack += 1
                        return True
                    else:
                        return False # Not added as reached max stack.
                else:
                    elist.append(event)
                    return True
            # Else if not found:
            elif not found:
                elist.append(event)
                return True
            else:
                return False
    except:
        print "Event error!"

def eAddHealthSelf(event, health):
    # Needs expanding:
    event.Owner.Health += (health / event.Middle.MaxDuration) * event.DT

def eNextStepPath(event):
    if event.Owner.Path:
        x, y = Libtcod.path_walk(event.Owner.Path, True)
        if not x is None:
            event.Owner.Move(x - event.Owner.X, y - event.Owner.Y)