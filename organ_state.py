#!/usr/bin/env python3

#Haven't yet assigned manual numbers to notes, so we will take naive approach
#(for now) of assuming 0 is lowest note on the manual

manual_list = ["swell","great","pedals"]

#A manual comes with its own unique (as far as I'm aware) switches. 
class Manual:
    def __init__(self, manual, *switches, NKEYS=128):
        if manual not in manual_list:
            print(f"{manual} not a recognised manual")
        self.manual = manual
        self.switch_set = [switch for switch in switches]
        self.switch_state = {rank:{} for rank in rank_names} 
        self.NKEYS = NKEYS
        self.state = [0]*self.NKEYS
        for switch in switches:
            if switch not in switch_names:
                print(f"{switch} not an available switch")
            for rank, rank_switches in ranks_and_switches.items():
                if switch in rank_switches.keys():
                    self.switch_state[rank].update({switch:
                        rank_switches[switch]})

        
#"organ rank":"switch name": [switch active, pipe pitch] 
#In this example we have four organ ranks and the switches that control them.
#The pipe pitch indicates how many notes above the bottom-most note will be
#played. Eg gems horn will raise every note played on the manual by 12 notes on
#the corresponding pipes(an octave)

#Note: The idea will be to fill this out with more organ ranks and switches to
#add more customisability for the user
ranks_and_switches =                    {"principal":{"open_diapason": [0, 0],
                                                      "gems_horn":     [0, 12],
                                                      "nazard":        [0, 19]},
                                         "wood":     {"lieblich":      [0, 0],
                                                      "gems_horn":     [0, 12]},
                                         "string":   {"salicional":    [0, 0],
                                                      "salicet":       [0,12]},
                                         "reed":     {"horn":          [0, 0],
                                                      "clarion":       [0,12],
                                                      "AndySwitch":    [0,42]}
}

switch_names = []

#get switch names from ranks_and_switches
for organ_rank, switches in ranks_and_switches.items():
    for switch_name in switches.keys():
        switch_names.append(switch_name)

rank_names = [key for key in ranks_and_switches.keys()]

organ_reset = ranks_and_switches.copy() 

pipe_state = {rank:[] for rank in rank_names}
#This stores instances of repeated pipe_ons for the same pipe 
pipe_cache = {rank:[] for rank in rank_names}

def init():
    global great_manual, swell_manual, pedal_manual

    #This is for demo purposes
    great_manual  = Manual("great","open_diapason","lieblich","salicional")
    swell_manual  = Manual("swell", "gems_horn","salicet", "horn")
    pedal_manual  = Manual("pedals", "nazard","clarion","AndySwitch")

#Get this working later
def reset():
    init()
    ranks_and_switches = organ_reset
    print(pipe_state)
    return

def update_pipes( manual,
                  key_number  = 0,
                  switch_name = "",
                  key_press   = False, 
                  key_release = False,
                  switch_on   = False,
                  switch_off  = False):

    if key_press == True:
        #check switch state to calculate pipes
        #can probably bundle this function into a class method later
        for rank, switches in manual.switch_state.items():
            for switch in switches:
                if switches[switch][0] == 1:
                    offset = switches[switch][1]
                    pipe_number = key_number + offset
                    if pipe_number not in pipe_state[rank]:
                        pipe_on(rank, pipe_number)
                    else:
                        pipe_cache[rank].append(pipe_number)

    if key_release == True:
        for rank, switches in manual.switch_state.items():
            for switch in switches:
                if switches[switch][0] == 1:
                    offset = switches[switch][1]
                    pipe_number = key_number + offset
                    #check duplicates first
                    if pipe_number in pipe_cache[rank]:
                        pipe_cache[rank].remove(pipe_number)
                    else:
                        pipe_off(rank, pipe_number)
        
    if switch_on == True:
        #check manual to calculate pipes
        manual_keys_on = []
        for i in range(manual.NKEYS):
            if manual.state[i] == 1:
                manual_keys_on.append(i)
        #Need to loop through ranks because of one to many relationship between
        #switches to pipes. Maybe something to change later? 
        for rank, switches in manual.switch_state.items():
            if switch_name in switches:
                offset = manual.switch_state[rank][switch_name][1]
                for key_number in manual_keys_on:
                    pipe_number = key_number + offset
                    if pipe_number not in pipe_state[rank]:
                        pipe_on(rank, pipe_number)

    if switch_off == True:
        manual_keys_on = []
        for i in range(manual.NKEYS):
            if manual.state[i] == 1:
                manual_keys_on.append(i)

        for rank, switches in manual.switch_state.items():
            if switch_name in switches:
                offset = manual.switch_state[rank][switch_name][1]
                for key_number in manual_keys_on:
                    pipe_number = key_number + offset
                    #first check pipe_cache
                    if pipe_number in pipe_cache[rank]:
                        pipe_cache[rank].remove(key_number)
                    else:
                        pipe_off(rank, pipe_number)
                        
    print(pipe_state)

def switch_toggle(manual, switch_name):
    if switch_name not in manual.switch_set:
        print(f"""{switch_name} not an available switch for the {manual.manual}
                   manual.Switchset is: {manual.switch_set}""")

    #update manual's switch_state 
    for rank, switches in manual.switch_state.items():
        if switch_name in switches:
            if switches[switch_name][0] == 1:
                print(f"Deactivating {switch_name} switch on {manual.manual}")
                manual.switch_state[rank][switch_name][0] = 0
                update_pipes( manual      = manual,
                              switch_name = switch_name,
                              switch_off  = True)
            else:
                print(f"Activating {switch_name} switch on {manual.manual}")
                manual.switch_state[rank][switch_name][0] = 1
                update_pipes( manual      = manual,
                              switch_name = switch_name,
                              switch_on   = True)

def key_press(manual, key):
    if (key >= manual.NKEYS) or (key < 0):
        print(f"keypress:{key} is an invalid key. Out of range 0-127")
        return
    if (manual.manual not in manual_list):
        print(f"keypress: {manual} not a recognised manual")
        return
    if manual.state[key] == 1:
        print(f"keypress: key {key} already active on {manual.manual} manual")
        return

    print(f"pressed key '{key}' on the {manual.manual} manual")
    manual.state[key] = 1
    update_pipes(key_number = key, manual = manual, key_press=True)

def key_release(manual, key):
    if (key >= manual.NKEYS) or (key < 0):
        print(f"keypress:{key} is an invalid key. Out of range 0-127")
        return
    if (manual.manual not in manual_list):
        print(f"keypress: {manual} not a recognised manual")
        return
    #check if key currently active
    if manual.state[key] != 1:
        print(f"key '{key}' not currently active on the {manual.manual} manual")
        return
    print(f"releasing key {key} on the {manual.manual} manual")
    manual.state[key] = 0
    update_pipes(key_number = key, manual = manual, key_release = True) 

def pipe_on(rank, pipe_number):
    print(f"activating pipe {pipe_number} on the {rank} rank")
    pipe_state[rank].append(pipe_number)

def pipe_off(rank, pipe_number):
    print(f"deactivating pipe {pipe_number} on the {rank} rank")
    pipe_state[rank].remove(pipe_number)

if __name__ == "__main__":

    init()
    switch_toggle(great_manual, "open_diapason")
    key_press(great_manual, 15)
    #test pressing the same key again
    key_press(great_manual, 15) 
    
    switch_toggle(swell_manual, "gems_horn")
    #This should activate pipe 15 on principal rank
    #because gems_horn raises the note by an octave (12)
    key_press(swell_manual, 3)
    key_press(swell_manual, 10)

    #we release key 15 on great manual, but pipe 15 on principal
    #should still be on
    key_release(great_manual, 15)
    #testing pressing a key on pedals. Pipe state shouldn't change
    #because none of the swell switches are active
    key_press(pedal_manual, 5)
    #Turn on AndySwitch 
    switch_toggle(pedal_manual, "AndySwitch")
    #Releasing key 3 on swell manual should deactivate pipe 15
    #on the principal rank
    key_release(swell_manual, 3)
    reset() 
