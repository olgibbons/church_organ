#!/usr/bin/env python3

#Need to think more broadly about initialising these

manual_list = ["swell","great","pedals"]
manual_state = {}

def init():
    #initialise manuals
    for manual in manual_list:
        manual_state[manual] = [0]*NKEYS
    #initialise pipeset for this specific scenario. Remove later

NKEYS = 128

class SwitchKey:
  def __init__(self, name, length, pipe, active=False):
        self.name = name
        self.length = length
        self.pipe = pipe
        self.active = active
  def to_dict(self):
     return {"name":self.name,"length":self.length,"pipe":self.pipe,
            "active":self.active}

class Switch:
  #I'm using a dictionary for quick-search purposes, but I imagine this is
  #overkill
  switch_names = {"open diapason": SwitchKey("open diapason", 8,   ["principal"]), #metal pipes
                  "lieblich":      SwitchKey("lieblich",      8,   ["wooden"]), #wooden
                  "salicional":    SwitchKey("salicional",    8,   ["string"]),#string
                  "gems-horn":     SwitchKey("gems-horn",     4,   ["wooden","principal"]),#both wooden and metal + 12 notes(octave)
                  "salicet":       SwitchKey("salicet",       4,   ["wooden"]),#string up octave
                  "nazard":        SwitchKey("nazard",        8/3, ["principal"]),#19 notes above open diapason
                  "horn":          SwitchKey("horn",          8,   ["reed"]),#reed
                  "clarion":       SwitchKey("clarion",       4,   ["reed"])}#octave above reed


  def __init__(self, number_of_switches=len(switch_names), manual="great"):
     if manual not in manual_list:
          print(f"{manual} not a recognised manual") 

     self.number_of_switches = number_of_switches
     self.manual = manual
     self.switch_state = self.number_of_switches*[0]
     self.switch_set = self.setup_switches() 
     self.pipe_set = self.setup_pipes()

  def setup_switches(self, *args):
    #Edit this later to create custom switch sets
    return self.switch_names

  def setup_pipes(self):
    pipeset = set()
    for name, switchkey in self.switch_names.items():
      for pipe in switchkey.pipe:
        pipeset.add(pipe)
    return {pipe: False for pipe in pipeset}
          
  def press_switch(self, name):
    if name not in self.switch_names.keys():
        print(f"press_switch: {name} is not a recognised switch key")
        return
    #activate switch in switch set
    self.switch_set[name].active = True
    print(f"{name} key has been activated")
    #set pipe to active. Need to send a signal to pipes later
    self.pipe

  
        

class Pipe:
    pipeList = ["principal","string","reed","wooden","flue","flute","hybrid"]
    def __init__(self, pipe, active=False):
        if pipe not in self.pipeList:
            print(f"Please enter a valid organ pipe: {self.pipeList}")
            return
        self.pipe = pipe
        self.active = active
        #Assuming a 1 to 1 relationship (unlikely)
        self.pipe_state =[0]*NKEYS 

    @classmethod
    def add_new_pipe(cls, newType):
        cls.pipeList.append(newType)

def createPipeSet(*args):
  return [Pipe(arg) for arg in args]


def keypress(key, manual):
    if (key >= NKEYS) or (key < 0):
        print(f"keypress:{key} is an invalid key. Out of range 0-127")
        return
    if (manual not in manual_list):
        print(f"keypress: {manual} not a recognised manual")
        return
    manual_state[manual][key] = 1

def keyrelease(key, manual):
    if (key >= NKEYS) or (key < 0): 
        print(f"keypress:{key} is an invalid key. Out of range 0-127")
        return
    if (manual not in manual_list):
        print(f"keypress: {manual} not a recognised manual")
        return
    manual_state[manual][key] = 0

#Any time something changes --> update pipes
# Any time switch/manual key pressed --> call update_pipes

def update_pipes(args*):
    #get manual output
    #get switch output
    #return organ state
    

if __name__=='__main__':
  
 init()
 newSwitchSet = Switch()
 print(newSwitchSet.pipe_set)
 newSwitchSet.press_switch("open diapason")
 print(newSwitchSet.switch_set["open diapason"].active)
